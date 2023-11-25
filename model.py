from sqlalchemy import Column, String, INT, BIGINT, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Booth(Base):
    __tablename__ = "booth"

    boothid = Column(BIGINT, nullable=False, autoincrement=True, primary_key=True)
    name = Column(String(collation="utf8mb4_unicode_ci"), nullable=False)
    boothcode = Column(INT, nullable=False)

class Menu(Base):
    __tablename__ = "menu"

    menuid = Column(BIGINT, nullable=False, autoincrement=True, primary_key=True)
    boothid = Column(BIGINT, ForeignKey("booth.boothid"), nullable=False)
    name = Column(String(collation="utf8mb4_unicode_ci"), nullable=False)
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
    email = Column(String(collation="utf8mb4_unicode_ci"), nullable=False)
    password = Column(INT, nullable=False)
    bank = Column(String(collation="utf8mb4_unicode_ci"), nullable=True)
    bankaccount = Column(String(collation="utf8mb4_unicode_ci"), nullable=True)
    bankbalance = Column(INT, nullable=True)

class Staff(Base):
    __tablename__ = "staff"

    staffid = Column(BIGINT, nullable=False, autoincrement=True, primary_key=True)
    boothid = Column(BIGINT, nullable=False)
    email = Column(String(collation="utf8mb4_unicode_ci"), nullable=False)
    password = Column(String(collation="utf8mb4_unicode_ci"), nullable=False)
    bank = Column(String(collation="utf8mb4_unicode_ci"), nullable=True)
    bankaccount = Column(String(collation="utf8mb4_unicode_ci"), nullable=True)
    bankbalance = Column(INT, nullable=True)