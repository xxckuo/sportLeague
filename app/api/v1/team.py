from flask import jsonify, request
from app.libs.redprint import Redprint
from app.models.base import db
from app.models.school import School
from app.libs.error_code import Success
from app.models.team import Team

api = Redprint('team')

@api.route('/create',methods=['POST'])
def create_team():
    jsonData = request.get_json()
    with db.auto_commit():
        team = Team()
        team.team_name = jsonData['team_name']
        team.team_logo = jsonData['team_logo']
        team.team_type = jsonData['team_type']
        team.team_captain = jsonData['team_captain']
        team.team_slogan = jsonData['team_slogan']
        team.team_comment = jsonData['team_comment']
        team.school_id = jsonData['school_id']
        team.category_id = jsonData['category_id']
        db.session.add(team)
    return Success(msg='新增成功')

@api.route('/update',methods=['POST'])
def update_team():
    jsonData = request.get_json()
    with db.auto_commit():
        team = Team.query.filter(Team.team_id == jsonData['team_id']).first()
        team.team_name = jsonData['team_name']
        team.team_logo = jsonData['team_logo']
        team.team_type = jsonData['team_type']
        team.team_captain = jsonData['team_captain']
        team.team_slogan = jsonData['team_slogan']
        team.team_comment = jsonData['team_comment']
        team.school_id = jsonData['school_id']
        team.category_id = jsonData['category_id']
    return Success(msg='修改成功')

@api.route('/get')
def get_team_by_id():
    team_id = request.args.get('team_id')
    team = Team.query.filter(Team.team_id==team_id).first_or_404()
    return Success(msg='查询成功',data=team.to_json())

@api.route('/getschoolteam')
def get_team_by_schoolid():
    # 根据学校来获取球队
    school_id = request.args.get('school_id')
    team = Team.query.filter(Team.school_id == school_id).all()
    school = Team.query.filter(School.school_id == school_id).first()
    datas={}
    datas['school'] = school.to_json()
    teams = []
    for tm in team:
        teams.append(tm.to_json())
    datas['team'] = teams
    return Success(msg='查询成功', data=datas)

@api.route('/delete',methods=['POST'])
def delete_team():
    # 禁用球队
    jsonData = request.get_json()
    with db.auto_commit():
        team = Team.query.filter(Team.team_id == jsonData['team_id']).first()
        team.team_name = 0
    return Success(msg='修改成功')
