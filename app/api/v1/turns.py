from flask import jsonify, request
from app.libs.redprint import Redprint
from app.models.base import db
from app.models.league import League
from app.models.school import School
from app.libs.error_code import Success
from app.models.turns import Turns

api = Redprint('turns')

@api.route('/create',methods=['POST'])
def create_turns():
    jsonData = request.get_json()
    with db.auto_commit():
        turns = Turns()
        turns.league_id = jsonData['league_id']
        turns.turns_name = jsonData['turns_name']
        db.session.add(turns)
    return Success(msg='新增轮次成功')

@api.route('/get')
def get_turns():
    # 通过赛事league_id查询出league_type赛事类型（联赛或者杯赛），根据league_id设置schedule_process返回到前端，
    # 在前端传新增赛程数据的时候传到后端，来区别这场比赛是联赛的比赛，还是杯赛的淘汰赛，还是小组赛
    league_id = request.args.get('league_id')
    league = db.session.query(League).filter(League.league_id == league_id)
    for l in league:
        print(l.to_json()['league_type'])
        schedule_process = 0 if l.to_json()['league_type'] == 1 else 2
    # 通过赛事league_id查询所有轮次
    turns = Turns.query.filter(Turns.league_id == league_id)
    allturns = []
    for tu in turns:
        temptu = tu.to_json()
        temptu['schedule_process'] = schedule_process
        allturns.append(temptu)
    return Success(msg='查找轮次成功', data=allturns)