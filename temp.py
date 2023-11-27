@app.get('/')
async def main():
    return {'results': 'success'}

'''GET'''

# 활성화된 부스 목록 확인하기
@app.get("/booth/get")
async def getBooth():
    booth = session.query(Booth).filter(Booth.state == 1).all()
    return booth

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
@app.get("/staff/get/")
async def getStaff(email: int):
    staff = session.query(Staff).filter(Staff.email == email).all()
    return staff