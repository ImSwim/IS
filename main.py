from fastapi import FastAPI
from dbconnection import engineconn
from model import Booth, Menu, Order_Menu

app: FastAPI = FastAPI() # FastAPI 모듈

engine = engineconn()
session = engine.sessionmaker()

@app.api_route('/', methods=['GET', 'DELETE'])
async def main():
    return {'success'}

'''GET'''

@app.get("/booth")
async def getBooth():
    booth = session.query(Booth).all()
    return booth

@app.get("/menu/{boothId}")
async def getMenu(boothId: int):
    menu = session.query(Menu).filter(Menu.boothid == boothId).all()
    return menu

@app.get("/order_menu/{boothId}")
async def getOrder_Menu(boothId: int):
    order_menu = session.query(Order_Menu).filter(Order_Menu.boothid == boothId).all()
    return order_menu


'''DELETE'''

@app.delete("/delete/{menuId}")
async def deleteMenu(menuId : int):
    session.query(Menu).filter(Menu.menuid == menuId).delete()
    session.commit()
    return {"message": "Menu deleted successfully"}