from sqlalchemy import Column, Integer, String, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base, db

class Turns(Base):
    turns_id = Column(Integer,primary_key=True, autoincrement=True,comment='杯赛1/8决赛，联赛第一轮id')
    league = relationship('League')
    league_id = Column(Integer, ForeignKey('league.league_id'),comment='所属赛事id')
    turns_name = Column(String(20),nullable=False,comment='杯赛1/8决赛，联赛第一轮')