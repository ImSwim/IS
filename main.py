from fastapi import FastAPI, HTTPException
from dbconnection import engineconn
from pydantic import BaseModel
from sqlalchemy import update
from model import Booth, Menu, Order_Menu, User, Staff

app: FastAPI = FastAPI() # FastAPI 모듈

engine = engineconn()
session = engine.sessionmaker()

@app.get('/')
async def main():
    return {'results': 'success'}

'''GET'''

# 활성화된 부스 목록 확인하기
@app.get("/get/booth")
async def getBooth():
    booth = session.query(Booth).filter(Booth.state == 1).all()
    return booth

# 특정 부스의 메뉴 목록 확인하기
@app.get("/menu/get/{boothId}")
async def getMenu(boothId: int):
    menu = session.query(Menu).filter(Menu.boothid == boothId).all()
    return menu

#주문 불이행 목록 확인하기
@app.get("/order_menu/get/{boothId}")
async def getOrder_Menu(boothId: int):
    order_menu = session.query(Order_Menu).filter((Order_Menu.boothid == boothId) & (Order_Menu.state == 0)).all()
    return order_menu


'''INSERT'''

# 주문 내역 DB에 넣기
class Order_Menu(BaseModel):
    userid : int
    boothid : int
    orderid : int
    menuid : int
    amount : int
    state : int

@app.post("/insert/order_menu")
async def insertOrder_Menu(order_menu: Order_Menu):
    try:
        session.add(order_menu)
        session.commit()
    except Exception as e:
        return {"message": f"Error inserting order menu: {str(e)}"}

    return {"message": "success"}


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
@app.get("/update/order_menu/{order_menuId}")
async def updateordermenu(order_menuId : int) :
    upordermenu = session.query(Order_Menu).filter(Order_Menu.order_menuid == order_menuId).first()
    if not upordermenu :
        return {"message": f"there is no order id: {order_menuId}"}
    session.execute(update(Order_Menu).where(Order_Menu.order_menuid == order_menuId).values(state=1))
    session.commit()

    return {"message": 'success'}

# 부스 상태 활성화 및 부스 아이디 반환
@app.get("/boothstate/update/{boothCode}")
async def updateordermenu(boothCode : int) :
    booth = session.query(Booth).filter(Booth.boothcode == boothCode).first()
    if not booth:
        return {"message": f"there is no booth for {boothCode}"}
    session.execute(update(Booth).where(Booth.boothid == boothCode).values(state=1))
    session.commit()

    return booth.boothid
