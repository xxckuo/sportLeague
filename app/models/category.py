from sqlalchemy import Column, Integer, String, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base, db

class Category(Base):
    category_id = Column(Integer,primary_key=True, autoincrement=True,comment='赛事类别id')
    category_name = Column(String(20),nullable=False,comment='篮球或者足球球队')