from sqlalchemy import Column, Integer, String, SmallInteger, ForeignKey,DateTime
from sqlalchemy.orm import relationship
from app.models.base import Base, db

class Player(Base):
    player_id = Column(Integer, primary_key=True, autoincrement=True,comment='球员id')
    player_name = Column(String(20),nullable=False,comment='球员姓名')
    player_sex = Column(SmallInteger,comment='1是男生，2是女生')
    player_picture = Column(String(80),nullable=True,comment='球员照片')
    player_place = Column(String(20),nullable=True,comment='位置，边卫')
    team = relationship('Team')
    team_id = Column(Integer, ForeignKey('team.team_id'),comment='球队id')
    player_age = Column(Integer,nullable=True,comment='球员年龄')
    player_number = Column(Integer,nullable=True,comment='球员球衣号码')
    player_height = Column(Integer,nullable=True,comment='球员身高')
    player_weight = Column(Integer,nullable=True,comment='球员体重')
    player_grade = Column(String(20),nullable=True,comment='球员年级，例如：大一')