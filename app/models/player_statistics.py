from sqlalchemy import Column, Integer, String, SmallInteger, ForeignKey,DateTime
from sqlalchemy.orm import relationship
from app.models.base import Base, db

class Player_statistics(Base):
    pt_id =  Column(Integer, primary_key=True, autoincrement=True,comment='球员统计id')
    player = relationship('Player')
    player_id = Column(Integer, ForeignKey('player.player_id'),comment='球员id')
    league = relationship('League')
    league_id = Column(Integer, ForeignKey('League.league_id'), comment='赛事id')
    team_name = Column(String(20),comment='球队名称')
    pt_score = Column(Integer, comment='进球',default=0)
    pt_assist = Column(Integer, comment='助攻',default=0)
    pt_foul = Column(Integer, comment='犯规',default=0)
    pt_yellow_card = Column(Integer, comment='黄牌',default=0)
    pt_red_card = Column(Integer, comment='红牌',default=0)

