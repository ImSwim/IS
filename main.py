from fastapi import FastAPI, HTTPException
from dbconnection import engineconn
from pydantic import BaseModel
from sqlalchemy import update
from model import Booth, Menu, OrderMenu, User, Staff, Order

app: FastAPI = FastAPI() # FastAPI 모듈

engine = engineconn()
session = engine.sessionmaker()

'''GET'''
# 특정 부스의 메뉴 목록 확인하기
@app.get("/menu/get/{boothId}")
async def getMenu(boothId: int):
    menu = session.query(Menu).filter(Menu.boothid == boothId).all()
    return menu

#주문 불이행 목록 확인하기
@app.get("/ordermenu/get/{boothId}")
async def getOrdermenu(boothId: int):
    ordermenu = session.query(OrderMenu).filter((OrderMenu.boothid == boothId) & (OrderMenu.state == 0)).all()
    return ordermenu

# 로그인
@app.get("/staff/get/{email}")
async def getStaff(email: str):
    staff = session.query(Staff).filter(Staff.email == email).all()
    if not staff:
        return {"message": f"there is no staff identified by {email}. check your email, and please log in again."}
    return staff

@app.get("/user/get/{email}")
async def getUser(email: str):
    user = session.query(User).filter(User.email == email).all()
    if not user:
        return {"message": f"there is no user identified by {email}. check your email, and please log in again."}
    return user

'''INSERT'''
# Menu 추가하기
class AddMenu(BaseModel):
    boothid: int
    name: str
    price: int

# 새로운 메뉴를 추가
@app.post("/menu/add/{boothid}")
async def add_menu(boothId: int, menu_data: AddMenu):

    try:
        # Use boothId from the path parameters
        menu_data.boothid = boothId
        # 여기서 "boothId" 대신 "boothid"를 사용
        new_menu = Menu(boothid = menu_data.boothid,
                        name = menu_data.name,
                        price = menu_data.price
                        )

        # 새로운 메뉴를 데이터베이스에 추가
        session.add(new_menu)
        session.commit()
        session.refresh(new_menu)

        return "Success"

    except Exception as e:
        # 에러가 발생한 경우 트랜잭션 롤백
        session.rollback()
        raise HTTPException(status_code=500, detail=f"내부 서버 오류: {str(e)}")

# ordermenu, order 데이터 저장하기

#pydantic models
class OrderMenuCreate(BaseModel):
    orderid : int
    menuid : int
    boothid : int
    amount : int
    state : int
class OrderCreate(BaseModel):
    boothid : int
    userid : int
    tablenumber : int
    totalprice : int
@app.get("/ordermenu/post")
async def postOrdermenu(ordermenus: list[OrderMenuCreate], order: OrderCreate):
    # order 먼저 저장
    session.add(order)
    session.commit()
    session.refresh(order)
    totalprice = 0
    # ordermenu 저장
    for ordermenu in ordermenus:
        dbordermenu = OrderMenu(
            orderid = order.orderid,
            menuid  = ordermenu.menuid,
            boothid = ordermenu.boothid,
            amount  = ordermenu.amount,
            state   = 0
        )
        # 주문 목록 개별 저장
        session.add(dbordermenu)
        session.commit()
        session.refresh(dbordermenu)

        menu = session.query(Menu).filter(Menu.id == ordermenu.menuid).first()                                          # 총 금액 계산
        totalprice += menu.price * ordermenu.amount

    # order total price update
    session.execute(update(Order).where(Order.orderid == order.orderid).values(totalprice=totalprice))
    session.commit()

    user = session.query(User).filter(User.id == order.userid).first()                                              # User 테이블과 Staff 테이블의 bankbalance 업데이트
    staff = session.query(Staff).filter((Staff.boothid == order.boothid) & (Staff.priority == 1)).first()

    if user.bankbalance < totalprice:                                                                                   # User 잔액이 부족한 경우 오류
        raise HTTPException(
            status_code=400,
            detail="Insufficient funds. first, please recharge your bank account.",
        )
    user.bankbalance -= totalprice
    staff.bankbalance += totalprice
    session.commit()

    return {"message": 'success'}

'''delete'''

# 메뉴 삭제하기
@app.delete("/delete/menu/{menuId}")
async def deleteMenu(menuId : int):
    menu = session.query(Menu).filter(Menu.menuid == menuId).first()
    if not menu:
        return {"message": f"there is no menu id : {menuId}"}
    session.delete(menu)
    session.commit()

    return {"message": 'success'}

'''Update'''

# 주문 이행 상태 업데이트
@app.get("/ordermenustate/update/{ordermenuId}")
async def updateOrdermenuState(ordermenuId : int) :
    upordermenu = session.query(OrderMenu).filter(OrderMenu.ordermenuid == ordermenuId).first()
    if not upordermenu:
        return {"message": f"there is no order id: {ordermenuId}"}
    session.execute(update(OrderMenu).where(OrderMenu.ordermenuid == ordermenuId).values(state=1))
    session.commit()

    return {"message": 'success'}

# 부스 상태 활성화 및 부스 아이디 반환
@app.get("/boothstate/update/{boothCode}")
async def updateBoothState(boothCode : int) :
    booth = session.query(Booth).filter(Booth.boothcode == boothCode).first()
    if not booth:
        return {"message": f"there is no booth for {boothCode}"}
    session.execute(update(Booth).where(Booth.boothid == boothCode).values(state=1))
    session.commit()

    return booth.boothid

# 사용자 계좌 잔액 충전
@app.get("/userbankbalance/update/{userId}/{chargeAmount}")
async def updateBoothState(userId : int, chargeAmount : int) :
    user = session.query(User).filter(User.userid == userId).first()
    if not user:
        return {"message": f"you should log-in again."}
    newbankbalance = 0
    newbankbalance += user.bankbalance + chargeAmount
    session.execute(update(User).where(User.userid == userId).values(bankbalance=newbankbalance))
    session.commit()
    session.refresh(user)
    return {"message": f"now your bankbalance is {user.bankbalance}."}
