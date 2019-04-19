from flask import jsonify, request
from app.libs.redprint import Redprint
from app.models.base import db
from app.libs.error_code import Success
from app.models.grade import Grade
from app.models.league import League
from app.models.team import Team

api = Redprint('league')


@api.route('/create_league', methods=['POST'])
def create_league():
    jsonData = request.get_json()
    with db.auto_commit():
        league = League()
        league.league_name = jsonData['league_name']
        league.league_type = jsonData['league_type']
        league.league_url = jsonData['league_url']
        league.category_id = jsonData['category_id']
        league.school_id = jsonData['school_id']
        db.session.add(league)
        #插入赛事的时候顺遍做一哈初始化，将积分榜里面插入的联赛成绩全部设为0
        if int(league.league_type) == 1:
            team_message = db.session.query(Team.team_id,Team.status).filter(Team.school_id == jsonData['school_id']).all()
            db.session.flush()
            for me in team_message:
                if me[1] == 1:
                    grade = Grade()
                    grade.grade_team = me[0]
                    #0是1，3，4就是查询出来的符合条件的队伍id
                    grade.league_id = league.league_id
                    grade.grade_turns = 0
                    grade.grade_win = 0
                    grade.grade_equal = 0
                    grade.grade_lose = 0
                    grade.grade_goal = 0
                    grade.grade_fumble =0
                    grade.grade_integral = 0
                    db.session.add(grade)
        return Success(msg='新增成功')


@api.route('/query_id')
def query_id():
    args = request.args.get("school_id")
    league_type = League.query.filter(League.school_id==args,League.status == 1).all()
    league_types = []
    for type in league_type:
        league_types.append(type.to_json())
    return Success(msg='查找成功', data=league_types)


@api.route('/query_type')
def query_type():
    args = request.args.get("league_type")
    league_type = League.query.filter(League.league_type==args).all()
    league_types = []
    for type in league_type:
        league_types.append(type.to_json())
    return Success(msg='查找成功', data=league_types)


@api.route('/delete_league')
def delete_league():
    args = request.args.get("league_id")
    with db.auto_commit():
        leagues = League.query.filter(League.league_id ==args).first()
        leagues.status = 0
    return Success(msg='删除成功')


@api.route('/update_league',methods=['POST'])
def update_league():
    jsonData = request.get_json()
    with db.auto_commit():
        leagues = League.query.filter(League.league_id == jsonData['league_id']).first()
        leagues.league_name = jsonData['league_name']
        leagues.league_type = jsonData['league_type']
        leagues.league_url = jsonData['league_url']
    return Success(msg='修改成功')
