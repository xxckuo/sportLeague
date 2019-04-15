from sqlalchemy import Column, Integer, String, SmallInteger, ForeignKey,Text
from sqlalchemy.orm import relationship
from app.models.base import Base, db

class Team(Base):
    team_id = Column(Integer, primary_key=True, autoincrement=True)
    team_name = Column(String(20),nullable=False,comment='球队名称')
    team_logo = Column(String(500),nullable=False,comment='球队图标')
    team_type = Column(SmallInteger,comment='1男，2女')
    team_captain = Column(Integer,nullable=True,comment='球队队长')
    team_slogan = Column(String(50),nullable=True,comment='球队口号')
    team_comment = Column(Text(500),nullable=True,comment='球队简介')
    school = relationship('School')
    school_id = Column(Integer, ForeignKey('school.school_id'),comment='学校id')
    category = relationship('Category')
    category_id = Column(Integer, ForeignKey('category.category_id'),comment='篮球或者足球球队')