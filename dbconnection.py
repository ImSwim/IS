from sqlalchemy import *
from sqlalchemy.orm import sessionmaker

DB_URL = 'mysql+pymysql://root:00000000@fiesta.c1xsexj6uj1i.us-east-1.rds.amazonaws.com:3306/fiesta' #RDS
#'mysql+pymysql://root:0000@127.0.0.1:3306/fiesta'  # 임수영 로컬 DB, 방화벽 열어둠

class engineconn:

    def __init__(self):
        self.engine = create_engine(DB_URL, pool_recycle = 500, encoding="utf-8")

    def sessionmaker(self):
        Session = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        session = Session()
        return session

    def connection(self):
        conn = self.engine.connect()
        return conn
