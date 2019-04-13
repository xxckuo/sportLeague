from flask import jsonify, request
from app.libs.redprint import Redprint
from app.models.base import db
from app.models.group import Group
from app.models.group_team import Group_team
from app.models.league import League
from app.models.school import School
from app.libs.error_code import Success
from app.models.team import Team

api = Redprint('group')

@api.route('/create',methods=['POST'])
def create_group():
    jsonData = request.get_json()
    with db.auto_commit():
        group = Group()
        group.group_name = jsonData['group_name']
        group.league_id = jsonData['league_id']
        db.session.add(group)
        for gt in  jsonData['group_team']:
            db.session.flush()
            group_team = Group_team()
            group_team.group_id = group.group_id
            group_team.league_id = jsonData['league_id']
            group_team.team_id = gt['team_id']
            db.session.add(group_team)
    return Success(msg='新增小组成功')

@api.route('/get')
def get_all_group_league_id():
    # 根据赛事id获取所有分组详细情况
    league_id = request.args.get('league_id')
    datas = []
    data = db.session.query(Group).filter(Group.league_id==league_id)
    for d in data:
        group_team = db.session.query(Group_team.gt_id,Team.team_name,Group_team.gt_win,
                                      Group_team.gt_equal,Group_team.gt_lose,Group_team.gt_goal,Group_team.gt_fumble,Group_team.gt_goal-Group_team.gt_fumble,Group_team.gt_integral).\
            filter(Group_team.league_id == league_id,Group_team.group_id==d.group_id,Group_team.team_id==Team.team_id).\
            order_by(Group_team.gt_integral.desc())
        tempdata = d.to_json()
        teams = []
        for t in group_team:
            m = {}
            m['gt_id'] = t[0]
            m['team_name'] = t[1]
            m['gt_win'] = t[2]
            m['gt_equal'] = t[3]
            m['gt_lose'] = t[4]
            m['gt_goal'] = t[5]
            m['gt_fumble'] = t[6]
            m['gt_gd'] = t[7]
            m['gt_integral'] = t[8] #积分
            teams.append(m)
        tempdata['group_team'] =teams
        datas.append(tempdata)
    return Success(msg='查询成功', data=datas)

@api.route('/getgroup')
def get_all_group_by_league_id():
    league_id = request.args.get('league_id')
    data = db.session.query(Group).filter(Group.league_id == league_id)
    returnDatas=[]
    for d in data:
        tempdata = d.to_json()
        tempdata['schedule_process'] = 1
        returnDatas.append(tempdata)
    return Success(msg='查询成功', data=returnDatas)