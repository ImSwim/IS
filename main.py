from fastapi import FastAPI
from sqlalchemy import select
from dbconnection import engineconn
from model import Booth, Menu, Order_Menu

app = FastAPI() # FastAPI 모듈

engine = engineconn()
session = engine.sessionmaker()

@app.get("/")
def index():
    return {
        "Success"
    }

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
