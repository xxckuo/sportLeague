from flask import request
from sqlalchemy import func

from app.libs.redprint import Redprint
from app.models.base import db
from app.libs.error_code import Success
from app.models.schedule import Schedule
from app.models.team import Team

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

# @api.route('/select', methods=['POST'])
# def schedule_select():
#     jsonData = request.get_json()
#     schedules = []
#     schedule = Schedule.query.filter_by(status=jsonData['status'],
#                     league_id=jsonData['league_id'])\
#         .order_by(Schedule.schedule_time)\
#         # .offset(jsonData['offset']).limit(jsonData['limit'])
#
#     for scs in schedule:
#         time = [scs.schedule_time]
#         time2=list(set(time))
#
#         print(time2)
#
#         group_team_a = db.session.query(Team.team_name, Team.team_logo). \
#                 filter(Team.team_id == scs.schedule_team_a)
#         group_team_b = db.session.query(Team.team_name, Team.team_logo). \
#             filter(Team.team_id == scs.schedule_team_b)
#
#         schedule_team = scs.to_json()
#
#         for team_b in group_team_b:
#             teamb = {}
#             teamb['teamb_name'] = team_b[0]
#             teamb['teamb_logo'] = team_b[1]
#             schedule_team['teamb_name']=team_b[0]
#             schedule_team['teamb_logo']=team_b[1]
#
#         for team_a in group_team_a:
#             teama = {}
#             teama['teama_name'] = team_a[0]
#             teama['teama_logo'] = team_a[1]
#             schedule_team['teama_name'] = team_a[0]
#             schedule_team['teama_logo'] = team_a[1]
#         schedules.append(schedule_team)
#     return Success(msg='查找成功', data=schedules)

@api.route('/select', methods=['POST'])
def schedule_select():

    jsonData = request.get_json()
    sc = db.session.query(func.FROM_UNIXTIME(Schedule.schedule_time,'%Y-%m-%d')).filter().group_by(
        func.FROM_UNIXTIME(Schedule.schedule_time,'%Y-%m-%d')).offset(jsonData['offset']).all()
    datas = {}
    for ssc in sc:

        ga = db.session.query(Schedule.schedule_id,Schedule.status,Schedule.league_id,Schedule.schedule_process,
                              Schedule.schedule_team_a,Schedule.schedule_team_b,Schedule.schedule_support_a,
                              Schedule.schedule_support_b,Schedule.schedule_score_a,Schedule.schedule_score_b,
                              Schedule.schedule_location,Schedule.schedule_judge,Schedule.schedule_status,
                              Schedule.schedule_turn_name)\
            .filter(func.FROM_UNIXTIME(Schedule.schedule_time,'%Y-%m-%d')==ssc[0]
                    ,Schedule.league_id==jsonData['league_id']
                    ).limit(jsonData['limit']).all()
        games=[]
        for g in ga:
            temp = {}
            temp['schedule_id'] = g[0]
            temp['league_status'] = g[1]
            temp['league_id'] = g[2]
            temp['schedule_process'] = g[3]
            temp['schedule_team_a'] = g[4]
            temp['schedule_team_b'] = g[5]
            temp['schedule_support_a'] = g[6]
            temp['schedule_support_b'] = g[7]
            temp['schedule_score_a'] = g[8]
            temp['schedule_score_b'] = g[9]
            temp['schedule_location'] = g[10]
            temp['schedule_judge'] = g[11]
            temp['schedule_status'] = g[12]
            temp['schedule_turn_name'] = g[13]
            games.append(temp)

            group_team_a = db.session.query(Team.team_name, Team.team_logo). \
                filter(Team.team_id == g[4])
            group_team_b = db.session.query(Team.team_name, Team.team_logo). \
                filter(Team.team_id == g[5])

            for team_a in group_team_a:
                temp['teama_name'] = team_a[0]
                temp['teama_logo'] = team_a[1]
            for team_b in group_team_b:
                temp['teamb_name'] = team_b[0]
                temp['teamb_logo'] = team_b[1]

        datas[ssc[0]] = games
    #
    return Success(msg='查找成功',data=datas)

