from sqlalchemy import Column, TEXT, INT, BIGINT, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Test(Base):
    __tablename__ = "test"

    id = Column(BIGINT, nullable=False, autoincrement=True, primary_key=True)
    name = Column(TEXT, nullable=False)
    number = Column(INT, nullable=False)

class Booth(Base):
    __tablename__ = "booth"

    boothid = Column(BIGINT, nullable=False, autoincrement=True, primary_key=True)
    name = Column(TEXT, nullable=False)

class Menu(Base):
    __tablename__ = "menu"

    menuid = Column(BIGINT, nullable=False, autoincrement=True, primary_key=True)
    boothid = Column(BIGINT, nullable=False)
    name = Column(TEXT, nullable=False)
    price = Column(INT, nullable=False)

class Order_Menu(Base):
    __tablename__ = "order_menu"

    orderid = Column(BIGINT, nullable=False, autoincrement=True, primary_key=True)
    menuid = Column(BIGINT, ForeignKey("menu.menuid"), nullable=False, autoincrement=True, primary_key=True)
    boothid = Column(BIGINT,  ForeignKey("booth.boothid"), nullable=False)
