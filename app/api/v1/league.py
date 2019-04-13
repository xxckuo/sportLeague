from flask import jsonify, request
from app.libs.redprint import Redprint
from app.models.base import db
from app.libs.error_code import Success
from app.models.league import League

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
        league.school_id= jsonData['school_id']

        db.session.add(league)
    return Success(msg='新增成功')


@api.route('/query_id')
def query_id():
    args = request.args.get("school_id")
    league_type = League.query.filter(League.school_id==args).all()
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


@api.route('/update_league')
def update_league():
    jsonData = request.get_json()
    with db.auto_commit():
        leagues = League.query.filter(League.league_id == jsonData['league_id']).first()
        leagues.league_name = jsonData['league_name']
        leagues.league_type = jsonData['league_type']
        leagues.league_url = jsonData['league_url']
    return Success(msg='修改成功')
