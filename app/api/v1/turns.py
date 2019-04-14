from flask import jsonify, request
from app.libs.redprint import Redprint
from app.models.base import db
from app.models.grade import Grade
from app.models.group_team import Group_team
from app.models.league import League
from app.models.schedule import Schedule
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