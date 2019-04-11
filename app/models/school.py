from sqlalchemy import Column, Integer, String, SmallInteger

from app.models.base import Base, db

class School(Base):
    school_id = Column(Integer, primary_key=True, autoincrement=True,comment='学校id')
    school_name = Column(String(50),unique=True,nullable=False,comment='学校名称')
    school_address = Column(String(50),nullable=False,comment='学校所在城市')