from sqlalchemy import Column, Integer, String, SmallInteger, ForeignKey,DateTime
from sqlalchemy.orm import relationship
from app.models.base import Base, db

class Grade(Base):
    # 积分榜
    grade_id = Column(Integer,primary_key=True, autoincrement=True,comment='积分榜id')
    league = relationship('League')
    league_id = Column(Integer, ForeignKey('league.league_id'),comment='赛事id')
    grade_team = Column(Integer,comment='球队id')
    grade_turns = Column(String(20),nullable=True,comment='杯赛1/8决赛，联赛第一轮')
    grade_win = Column(Integer, comment='胜',default=0)
    grade_equal = Column(Integer, comment='平',default=0)
    grade_lose = Column(Integer, comment='负',default=0)
    grade_goal = Column(Integer, comment='进球',default=0)
    grade_fumble = Column(Integer, comment='失球',default=0)
    grade_integral = Column(Integer, comment='积分',default=0)