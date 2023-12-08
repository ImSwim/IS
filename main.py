from fastapi import FastAPI, HTTPException
from dbconnection import engineconn
from pydantic import BaseModel
from sqlalchemy import update
from typing import List, Optional
from model import *

app: FastAPI = FastAPI() # FastAPI 모듈

engine = engineconn()
session = engine.sessionmaker()

@app.get("/")
async def Main():
    return {"message": 'success'}

'''GET'''
@app.get("/booth/get")
async def getBooth():
    booth = session.query(Booth).filter(Booth.state == 1).all()
    return booth
# 부스 상태 확인 및 부스 객체 반환
@app.get("/booth/get/{boothCode}")
async def getBoothbyCode(boothCode : int) :
    booth = session.query(Booth).filter(Booth.boothcode == boothCode).first()
    if not booth:
        return {"message": f"there is no booth identified by {boothCode}"}
    else:
        if booth.state == 1:
            return booth
        else:
            return {"message": f"booth is not activated. login as 1st staff at first."}

# 특정 부스의 메뉴 목록 확인하기
@app.get("/menu/get/{boothId}")
async def getMenu(boothId: int):
    menu = session.query(Menu).filter(Menu.boothid == boothId).all()
    return menu

#주문 불이행 목록 확인하기
@app.get("/ordermenu/get/{boothId}")
async def getOrdermenu(boothId: int):
    ordermenu = session.query(OrderMenu).filter((OrderMenu.boothid == boothId) & (OrderMenu.state == int(0))).all()
    return ordermenu

# 로그인, 회원 정보 수정 등에 사용
@app.get("/staff/get/{email}")
async def getStaff(email: str):
    staff = session.query(Staff).filter(Staff.email == email).first()
    if not staff:
        return {"message": f"there is no staff identified by {email}. check your email, and please log in again."}
    return staff

@app.get("/user/get/{email}")
async def getUser(email: str):
    user = session.query(User).filter(User.email == email).first()
    if not user:
        return {"message": f"there is no user identified by {email}. check your email, and please log in again."}
    return user

'''INSERT'''
# Menu 추가하기
class MenuCreate(BaseModel):
    boothid: int
    name: str
    price: int

# 새로운 메뉴를 추가
@app.post("/menu/post")
async def postMenu(menu_data: MenuCreate):

    try:
        new_menu = Menu(boothid = menu_data.boothid,
                        name = menu_data.name,
                        price = menu_data.price
                        )

        # 새로운 메뉴를 데이터베이스에 추가
        session.add(new_menu)
        session.commit()
        session.refresh(new_menu)

        return {"message": 'success'}

    except Exception as e:
        # 에러가 발생한 경우 트랜잭션 롤백
        session.rollback()
        raise HTTPException(status_code=500, detail=f"내부 서버 오류: {str(e)}")

# ordermenu, order 데이터 저장하기

#pydantic models
class OrderMenuCreate(BaseModel):
    orderid : Optional[int] = None
    menuid : int
    boothid : int
    amount : int
    state : Optional[int] = 0
class OrderCreate(BaseModel):
    boothid : int
    userid : int
    tablenumber : int
    totalprice : Optional[int] = 0
@app.post("/ordermenu/post")
async def postOrdermenu(ordermenus: List[OrderMenuCreate], order: OrderCreate):
    # order 먼저 저장
    dborder = Order(
            boothid  = order.boothid,
            userid = order.userid,
            tablenumber  = order.tablenumber,
            totalprice   = order.totalprice
        )
    session.add(dborder)
    session.commit()
    session.refresh(dborder)
    
    totalprice = 0
    # ordermenu 저장
    for ordermenu in ordermenus:
        dbordermenu = OrderMenu(
            orderid = dborder.orderid,
            menuid  = ordermenu.menuid,
            boothid = ordermenu.boothid,
            amount  = ordermenu.amount,
            state   = 0
        )
        # 주문 목록 개별 저장
        session.add(dbordermenu)
        session.commit()
        session.refresh(dbordermenu)

        menu = session.query(Menu).filter(Menu.menuid == ordermenu.menuid).first()                                          # 총 금액 계산
        totalprice += menu.price * ordermenu.amount

    # order total price update
    session.execute(update(Order).where(Order.orderid == dborder.orderid).values(totalprice=totalprice))
    session.commit()

    user = session.query(User).filter(User.userid == dborder.userid).first()                                              # User 테이블과 Staff 테이블의 bankbalance 업데이트
    staff = session.query(Staff).filter((Staff.boothid == dborder.boothid) & (Staff.priority == 1)).first()

    if user.bankbalance < totalprice:                                                                                   # User 잔액이 부족한 경우 오류
        raise HTTPException(
            status_code=400,
            detail="Insufficient funds. first, please recharge your bank account.",
        )
    user.bankbalance -= totalprice
    staff.bankbalance += totalprice
    session.execute(update(User).where(User.userid == user.userid).values(bankbalance=user.bankbalance))
    session.execute(update(Staff).where(Staff.staffid == staff.staffid).values(bankbalance=staff.bankbalance))
    session.commit()

    return totalprice

## POST USER
class UserCreate(BaseModel):
    email: str
    password: str
    bank: str
    bankaccount : str
    bankbalance : Optional[int] = int(0)

# 새로운 유저를 추가
@app.post("/user/post")
async def postUser(user_data: UserCreate):

    try:
        new_user = User(email = user_data.email,
                        password = user_data.password,
                        bank = user_data.bank,
                        bankaccount = user_data.bankaccount,
                        bankbalance = user_data.bankbalance
                        )

        # 새로운 유저저를 데이터베이스에 추가
        session.add(new_user)
        session.commit()
        session.refresh(new_user)

        return {"message": 'success'}

    except Exception as e:
        # 에러가 발생한 경우 트랜잭션 롤백
        session.rollback()
        raise HTTPException(status_code=500, detail=f"내부 서버 오류: {str(e)}")
        
## POST STAFF
class StaffCreate(BaseModel):
    boothid : int
    email: str
    password: str
    bank: str
    bankaccount : str
    bankbalance : Optional[int] = int(0)
    priority : int

# 새로운 스태프프를 추가
@app.post("/staff/post")
async def postStaff(staff_data: StaffCreate):
    try:
        new_staff = Staff(boothid = staff_data.boothid,
                    email = staff_data.email,
                    password = staff_data.password,
                    bank = staff_data.bank,
                    bankaccount = staff_data.bankaccount,
                    bankbalance = int(0),
                    priority = staff_data.priority
                    )

    # 새로운 스태프프를 데이터베이스에 추가
        session.add(new_staff)
        session.commit()
        session.refresh(new_staff)

        return {"message": 'success'}

    except Exception as e:
        # 에러가 발생한 경우 트랜잭션 롤백
        session.rollback()
        raise HTTPException(status_code=500, detail=f"내부 서버 오류: {str(e)}")
        
        
''' PUT(UPDATE) '''
class UserCreate(BaseModel):
    email : str
    password :str
    bank : str
    bankaccount : str
    bankbalance : int

class StaffCreate(BaseModel):
    email: str
    password: str
    bank: Optional[str] = None
    bankaccount: Optional[str] = None
    bankbalance: Optional[int] = None

# 회원정보 수정하기
@app.put("/user/update/{email}")
def updateUser(email: str, updated_info: UserCreate):
    user = session.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

    # 업데이트할 필드가 허용된 필드인지 확인하고 업데이트
    for key, value in updated_info.dict().items():
        if value is not None:
            setattr(user, key, value)
        else:
            raise HTTPException(status_code=400, detail=f"'{key}' 필드는 필수 입력값입니다.")

    session.commit()
    session.refresh(user)

    return user

@app.put("/staff/update/{email}")
def updateStaff(email: str, updated_info: StaffCreate):
    try:
        staff = session.query(Staff).filter(Staff.email == email).first()
        if staff is None:
            raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

        # 정보를 업데이트하기 전에 priority를 확인
        priority_value = int(staff.priority.decode('utf-8'))
        if priority_value == 0:
            # priority가 0인 경우에는 허용된 필드만 업데이트
            allowed_fields = ["email", "password", "bank", "bankaccount", "bankbalance"]
        elif priority_value == 1:
            # priority가 1인 경우에는 email과 password만 업데이트
            allowed_fields = ["email", "password"]
        else:
            raise HTTPException(status_code=400, detail="잘못된 priority 값입니다.")
        # 업데이트할 필드가 허용된 필드인지 확인하고 업데이트
        for key, value in updated_info.dict().items():
            if key in allowed_fields:
                setattr(staff, key, value)

        session.commit()
        session.refresh(staff)

        return staff
    
    except Exception as e:
        print(f"An error occurred: {e}")
        raise


# 주문 이행 상태 업데이트
@app.put("/ordermenustate/update/{ordermenuId}")
async def updateOrdermenuState(ordermenuId : int) :
    upordermenu = session.query(OrderMenu).filter(OrderMenu.ordermenuid == ordermenuId).first()
    if not upordermenu:
        return {"message": f"there is no order id: {ordermenuId}"}
    session.execute(update(OrderMenu).where(OrderMenu.ordermenuid == ordermenuId).values(state=1))
    session.commit()
    ordermenu = session.query(OrderMenu).filter(OrderMenu.ordermenuid == ordermenuId).first()
    return ordermenu

# 부스 상태 활성화 및 부스 아이디 반환
@app.put("/boothstate/update/{boothCode}")
async def updateBoothState(boothCode : int) :
    booth = session.query(Booth).filter(Booth.boothcode == boothCode).first()
    if not booth:
        return {"message": f"there is no booth identified by {boothCode}"}
    else:
        session.execute(update(Booth).where(Booth.boothcode == boothCode).values(state=1))
        session.commit()
        booth = session.query(Booth).filter(Booth.boothcode == boothCode).first()
        return booth

# 사용자 계좌 잔액 충전
@app.put("/userbankbalance/update/{userId}/{chargeAmount}")
async def updateUserBankbalance(userId : int, chargeAmount : int) :
    user = session.query(User).filter(User.userid == userId).first()
    if not user:
        return {"message": f"you should log-in again."}
    newbankbalance = 0
    newbankbalance += user.bankbalance + chargeAmount
    session.execute(update(User).where(User.userid == userId).values(bankbalance=newbankbalance))
    session.commit()
    session.refresh(user)
    return user


'''delete'''

# 메뉴 삭제하기
@app.delete("/menu/delete/{menuId}")
async def deleteMenu(menuId : int):
    menu = session.query(Menu).filter(Menu.menuid == menuId).first()
    if not menu:
        return {"message": f"there is no menu id : {menuId}"}
    session.delete(menu)
    session.commit()
    return {"message": "success"}

