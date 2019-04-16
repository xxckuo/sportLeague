from flask import request
from sqlalchemy import func

from app.libs.redprint import Redprint
from app.models.base import db
from app.libs.error_code import Success
from app.models.grade import Grade
from app.models.group_team import Group_team
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



@api.route('/select', methods=['POST'])
def schedule_select():

    jsonData = request.get_json()
    sc = db.session.query(func.FROM_UNIXTIME(Schedule.schedule_time,'%Y-%m-%d')).filter().group_by(
        func.FROM_UNIXTIME(Schedule.schedule_time,'%Y-%m-%d')).offset(jsonData['offset']).limit(jsonData['limit']).all()
    datas = {}
    for ssc in sc:

        ga = db.session.query(Schedule.schedule_id,Schedule.status,Schedule.league_id,Schedule.schedule_process,
                              Schedule.schedule_team_a,Schedule.schedule_team_b,Schedule.schedule_support_a,
                              Schedule.schedule_support_b,Schedule.schedule_score_a,Schedule.schedule_score_b,
                              Schedule.schedule_location,Schedule.schedule_judge,Schedule.schedule_status,
                              Schedule.schedule_turn_name,Schedule.schedule_time)\
            .filter(func.FROM_UNIXTIME(Schedule.schedule_time,'%Y-%m-%d')==ssc[0]
                    ,Schedule.league_id==jsonData['league_id']
                    ).all()
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
            temp['schedule_time'] = g[14]
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

@api.route('/update_schedule',methods=['POST'])
def update_schedule():
    jsonData = request.get_json()
    with db.auto_commit():
        sc = Schedule.query.filter(Schedule.schedule_id == jsonData['schedule_id']).first()
        sc.schedule_score_a = jsonData['schedule_score_a']
        sc.schedule_score_b = jsonData['schedule_score_b']
        sc.schedule_status = jsonData['schedule_status']

    if jsonData['schedule_process'] == '0':
        with db.auto_commit():
            gda = Grade.query.filter(Grade.grade_team == jsonData['schedule_team_a'],Grade.league_id == jsonData['league_id']).first()
            gdb = Grade.query.filter(Grade.grade_team == jsonData['schedule_team_b'],Grade.league_id == jsonData['league_id']).first()
            gda.grade_goal = jsonData['schedule_score_a']
            gda.grade_fumble = jsonData['schedule_score_b']
            gda.grade_turns = int(gda.grade_turns)+1

            gdb.grade_goal = jsonData['schedule_score_b']
            gdb.grade_fumble = jsonData['schedule_score_a']
            gdb.grade_turns = int(gdb.grade_turns) + 1

            if int(jsonData['schedule_score_a']) > int(jsonData['schedule_score_b']):
                gda.grade_win = int(gda.grade_win)+1
                gdb.grade_lose = int(gdb.grade_lose) + 1
                gda.grade_integral = int(gda.grade_integral)+3
            elif int(jsonData['schedule_score_a']) < int(jsonData['schedule_score_b']):
                gdb.grade_win = int(gdb.grade_win) + 1
                gda.grade_lose = int(gda.grade_lose) + 1
                gdb.grade_integral = int(gdb.grade_integral) + 3
            else:
                gda.grade_equal = int(gdb.grade_equal) + 1
                gdb.grade_equal = int(gdb.grade_equal) + 1
                gda.grade_integral = int(gda.grade_integral) + 1
                gdb.grade_integral = int(gdb.grade_integral) + 1
    elif jsonData['schedule_process'] == '1':
        with db.auto_commit():
            gda = Group_team.query.filter(Group_team.team_id == jsonData['schedule_team_a'],
                                          Group_team.league_id == jsonData['league_id']).first()
            gdb = Group_team.query.filter(Group_team.team_id == jsonData['schedule_team_b'],
                                          Group_team.league_id == jsonData['league_id']).first()
            gda.gt_goal = jsonData['schedule_score_a']
            gda.gt_fumble = jsonData['schedule_score_b']

            gdb.gt_goal = jsonData['schedule_score_b']
            gdb.gt_fumble = jsonData['schedule_score_a']

            if int(jsonData['schedule_score_a']) > int(jsonData['schedule_score_b']):
                gda.gt_win = int(gda.gt_win) + 1
                gdb.gt_lose = int(gdb.gt_lose) + 1
                gda.gt_integral = int(gda.gt_integral) + 3
            elif int(jsonData['schedule_score_a']) < int(jsonData['schedule_score_b']):
                gdb.gt_win = int(gdb.gt_win) + 1
                gda.gt_lose = int(gda.gt_lose) + 1
                gdb.gt_integral = int(gdb.gt_integral) + 3
            else:
                gda.gt_equal = int(gdb.gt_equal) + 1
                gdb.gt_equal = int(gdb.gt_equal) + 1
                gda.gt_integral = int(gda.gt_integral) + 1
                gdb.gt_integral = int(gdb.gt_integral) + 1
    return Success(msg='修改比分成功')

