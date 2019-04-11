from sqlalchemy import Column, Integer, String, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base, db

class Group_team(Base):
    gt_id = Column(Integer,primary_key=True, autoincrement=True,comment='杯赛小组球队id')
    group = relationship('Group')
    group_id = Column(Integer, ForeignKey('group.group_id'),comment='属于哪个小组')
    team = relationship('Team')
    team_id = Column(Integer, ForeignKey('team.team_id'),comment='球队id')
    gt_win = Column(Integer,comment='胜',default=0)
    gt_equal = Column(Integer,comment='平',default=0)
    gt_lose = Column(Integer, comment='负',default=0)
    gt_goal = Column(Integer, comment='进球',default=0)
    gt_fumble = Column(Integer, comment='失球',default=0)
    gt_integral = Column(Integer, comment='积分',default=0)