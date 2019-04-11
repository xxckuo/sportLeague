from sqlalchemy import Column, Integer, String, SmallInteger,ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base, db

class School_admin(Base):
    sa_id = Column(Integer, primary_key=True, autoincrement=True,comment='管理员ID')
    school = relationship('School')
    school_id = Column(Integer, ForeignKey('school.school_id'),comment='管理员所在学校id')
    sa_account = Column(Integer, unique=True, nullable=False,comment='管理员账号，手机号')
    sa_name = Column(String(20), nullable=False,comment='管理员姓名')
    sa_password = Column(String(20), nullable=False,comment='管理员密码')
