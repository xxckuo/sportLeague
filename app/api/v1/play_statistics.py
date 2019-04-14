from flask import  request
from sqlalchemy import desc

from app.libs.redprint import Redprint
from app.models.base import db
from app.libs.error_code import Success
from app.models.player_statistics import Player_statistics

api = Redprint('play_statistics')

@api.route('/create', methods=['POST'])
def play_statistics_create():
    jsonData = request.get_json()
    with db.auto_commit():
        play_statistics = Player_statistics()

        play_statistics.player_id = jsonData['player_id']
        play_statistics.team_name= jsonData['team_name']
        play_statistics.pt_score = jsonData['pt_score']
        play_statistics.pt_assist = jsonData['pt_assist']
        play_statistics.pt_foul = jsonData['pt_foul']
        play_statistics.pt_yellow_card = jsonData['pt_yellow_card']
        play_statistics.pt_red_card = jsonData['pt_red_card']

        db.session.add(play_statistics)
    return Success(msg='新增球员积分榜成功')

@api.route('/select',methods = ['GET'])
def play_select():
    select = request.args.get('select')
    play = Player_statistics.query.order_by(desc(select))
    plays = []
    for sc in play:
        plays.append(sc.to_json())
    return Success(msg='查找球员积分榜成功', data=plays)