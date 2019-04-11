from sqlalchemy import Column, Integer, String, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base, db

class Group(Base):
    group_id = Column(Integer,primary_key=True, autoincrement=True,comment='组别id，A组，B组')
    league = relationship('League')
    league_id = Column(Integer,ForeignKey('league.league_id'),comment='赛事id，只属于杯赛')
    group_name = Column(String(20),comment='A组')