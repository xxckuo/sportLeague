from flask import request

from app.libs.redprint import Redprint
from app.models.base import db
from app.libs.error_code import Success
from app.models.schedule import Schedule

api = Redprint('schedule')

@api.route('/create', methods=['POST'])
def schedule_create():
    jsonData = request.get_json()
    with db.auto_commit():
        schedule =Schedule()
        schedule.league_id = jsonData['league_id']
        schedule.schedule_process = jsonData['schedule_process']
        schedule.schedule_team_a = jsonData['schedule_team_a']
        schedule.schedule_team_b = jsonData['schedule_team_b']
        schedule.schedule_support_a = jsonData['schedule_support_a']
        schedule.schedule_support_b = jsonData['schedule_support_b']
        schedule.schedule_score_a = jsonData['schedule_score_a']
        schedule.schedule_score_b= jsonData['schedule_score_b']
        schedule.schedule_location = jsonData['schedule_location']
        schedule.schedule_time = jsonData['schedule_time']
        schedule.schedule_judge = jsonData['schedule_judge']
        schedule.schedule_status = jsonData['schedule_status']
        schedule.schedule_turn_name = jsonData['schedule_turn_name']
        db.session.add(schedule)
    return Success(msg='新增赛事成功')

@api.route('/select', methods=['GET'])
def schedule_select():
    # 根据league_id查找联赛或者杯赛
    league_id = request.args.get('league_id')
    schedule = Schedule.query.group_by('schedule_time').all()
    for sc in schedule:
        print(sc)
    # schedules = []
    # for sc in schedule:
    #     schedules.append(sc.to_json())
    # return Success(msg='查找成功', data=schedules)
    return 'hello'
