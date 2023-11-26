from sqlalchemy import Column, String, Integer, BigInteger, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Booth(Base):
    __tablename__ = "booth"

    boothid = Column(BigInteger, nullable=False, autoincrement=True, primary_key=True)
    name = Column(String, nullable=False)
    boothcode = Column(Integer, nullable=False)
    state = Column(Integer, nullable=False)

    # 인용당함
    staffs = relationship('Staff', back_populates='booths')
    orders = relationship('Order', back_populates='booths')
    menus = relationship('Menu', back_populates='booths')
    order_menus = relationship('Order_Menu', back_populates='booths')

class Menu(Base):
    __tablename__ = "menu"

    menuid = Column(BigInteger, nullable=False, autoincrement=True, primary_key=True)
    boothid = Column(BigInteger, ForeignKey("booth.boothid"), nullable=False)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    # 인용함
    booths = relationship('Booth', back_populates='menus')
    # 인용 당함
    order_menus = relationship('Order_Menu', back_populates='menus')

class Order(Base):
    __tablename__ = "order"

    orderid = Column(BigInteger, nullable=False, autoincrement=True, primary_key=True)
    boothid = Column(BigInteger,  ForeignKey("booth.boothid"), nullable=False)
    userid = Column(BigInteger,  ForeignKey("user.userid"), nullable=False)
    tablenumber = Column(Integer, nullable=False)
    totalprice = Column(Integer, nullable=False)

    # 인용함
    booths = relationship('Booth', back_populates='orders')
    users = relationship('User', back_populates='orders')

    #인용 당함
    order_menus = relationship('Order_Menu', back_populates='orders')

class Order_Menu(Base):
    __tablename__ = "order_menu"

    order_menuid = Column(BigInteger, nullable=False, autoincrement=True, primary_key=True)
    orderid = Column(BigInteger, ForeignKey("order.orderid"), nullable=False)
    menuid = Column(BigInteger, ForeignKey("menu.menuid"), nullable=False)
    boothid = Column(BigInteger,  ForeignKey("booth.boothid"), nullable=False)
    amount = Column(Integer, nullable=False)
    state = Column(Integer, nullable=False)

    # 인용함
    booths = relationship('Booth', back_populates='order_menus')
    menus = relationship('Menu', back_populates='order_menus')
    orders = relationship('Order', back_populates='order_menus')
###########

class User(Base):
    __tablename__ = "user"

    userid = Column(BigInteger, nullable=False, autoincrement=True, primary_key=True)
    email = Column(String, nullable=False)
    password = Column(Integer, nullable=False)
    bank = Column(String, nullable=True)
    bankaccount = Column(String, nullable=True)
    bankbalance = Column(Integer, nullable=True)

    # 인용 당함
    orders = relationship('Order', back_populates='users')

class Staff(Base):
    __tablename__ = "staff"

    staffid = Column(BigInteger, nullable=False, autoincrement=True, primary_key=True)
    boothid = Column(BigInteger, ForeignKey("booth.boothid"), nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    bank = Column(String, nullable=True)
    bankaccount = Column(String, nullable=True)
    bankbalance = Column(Integer, nullable=True)
    priority = Column(Integer, nullable=False)

    booths = relationship('Booth', back_populates='staffs')
