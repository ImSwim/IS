from sqlalchemy import Column, TEXT, INT, BIGINT, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Booth(Base):
    __tablename__ = "booth"

    boothid = Column(BIGINT, nullable=False, autoincrement=True, primary_key=True)
    name = Column(TEXT, nullable=False)
    boothcode = Column(INT, nullable=False)

class Menu(Base):
    __tablename__ = "menu"

    menuid = Column(BIGINT, nullable=False, autoincrement=True, primary_key=True)
    boothid = Column(BIGINT, nullable=False)
    name = Column(TEXT, nullable=False)
    price = Column(INT, nullable=False)

class Order_Menu(Base):
    __tablename__ = "order_menu"

    order_menuid = Column(BIGINT, nullable=False, autoincrement=True, primary_key=True)
    orderid = Column(BIGINT, ForeignKey("order.orderid"), nullable=False)
    menuid = Column(BIGINT, ForeignKey("menu.menuid"), nullable=False)
    boothid = Column(BIGINT,  ForeignKey("booth.boothid"), nullable=False)

###########

class User(Base):
    __tablename__ = "user"

    userid = Column(BIGINT, nullable=False, autoincrement=True, primary_key=True)
    email = Column(TEXT, nullable=False)
    password = Column(INT, nullable=False)
    bank = Column(TEXT, nullable=True)
    bankaccount = Column(TEXT, nullable=True)
    bankbalance = Column(INT, nullable=True)

class Staff(Base):
    __tablename__ = "staff"

    staffid = Column(BIGINT, nullable=False, autoincrement=True, primary_key=True)
    boothid = Column(BIGINT, nullable=False)
    email = Column(TEXT, nullable=False)
    password = Column(INT, nullable=False)
    bank = Column(TEXT, nullable=True)
    bankaccount = Column(TEXT, nullable=True)
    bankbalance = Column(INT, nullable=True)