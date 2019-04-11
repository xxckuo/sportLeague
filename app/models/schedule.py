from sqlalchemy import Column, Integer, String, SmallInteger, ForeignKey,DateTime
from sqlalchemy.orm import relationship
from app.models.base import Base, db

class Schedule(Base):
    # 赛程表
    schedule_id = Column(Integer,primary_key=True, autoincrement=True,comment='赛程id')
    league = relationship('League')
    league_id = Column(Integer, ForeignKey('league.league_id'),comment='赛事id')
    team = relationship('Team')
    schedule_team_a = Column(Integer, ForeignKey('team.team_id'),comment='球队Aid')
    schedule_team_b = Column(Integer, ForeignKey('team.team_id'),comment='球队Bid')
    schedule_support_a = Column(Integer,default=0,comment='球队A支持数')
    schedule_support_b = Column(Integer, default=0,comment='球队B支持数')
    schedule_score_a = Column(Integer, default=0,comment='球队A得分')
    schedule_score_b = Column(Integer, default=0,comment='球队B得分')
    schedule_location = Column(String(20),nullable=False,comment='比赛地点')
    schedule_time = Column(DateTime,comment='比赛时间')
    schedule_judge = Column(String(20),nullable=True,comment='裁判，举例：裁判1，裁判2，裁判3')
    schedule_status = Column(SmallInteger,default=0,comment='0为未开赛，1为进行中，2已结束')
    schedule_turn_name = Column(String(20),comment='杯赛1/8决赛，联赛第一轮')