from sqlalchemy import Column, Integer, String, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base, db

class League(Base):
    league_id = Column(Integer,primary_key=True, autoincrement=True, comment='赛事id')
    league_name = Column(String(20),nullable=False,comment='赛事名称')
    league_type = Column(SmallInteger,nullable=False,comment='赛事类型1是联赛，2是杯赛')
    school = relationship('School')
    school_id = Column(Integer, ForeignKey('school.school_id'),comment='学校id')
    league_url = Column(String(500),nullable=False)
    category = relationship('Category')
    category_id = Column(Integer,ForeignKey('category.category_id'),comment='赛事类型，举例：篮球或者足球')