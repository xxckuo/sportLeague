from flask import jsonify, request
from app.libs.redprint import Redprint
from app.models.base import db
from app.libs.error_code import Success
from app.models.grade import Grade
from app.models.team import Team

api = Redprint('grade')
@api.route('/display_grade')
def display_grade():
    league_id = request.args.get('league_id')
    data = db.session.query(Grade).filter(Grade.league_id == league_id)
    for d in data:
        team = db.session.query(Grade.grade_id,Grade.grade_team,Grade.grade_turns,Grade.grade_win,Grade.grade_equal
                                ,Grade.grade_lose,Grade.grade_goal,Grade.grade_fumble,Grade.grade_integral,Team.team_logo,Team.team_name).\
        filter(Grade.league_id == league_id,Team.team_id == d.grade_team). \
            order_by(Grade.grade_integral.desc())
        tempdata = d.to_json()
        teams = []
        for b in team:
            d={}
            d['grade_id'] = b[0]
            d['grade_team'] = b[1]
            d['grade_turns'] = b[2]
            d['grade_win'] = b[3]
            d['grade_equal'] = b[4]
            d['grade_lose'] = b[5]
            d['grade_goal'] = b[6]
            d['grade_fumble'] = b[7]
            d['grade_integral'] = b[8]
            d['team_logo']=b[9]
            d['team_name']=b[10]
            teams.append(d)
            tempdata['grade_team'] = teams
        return Success(msg='查询成功', data=teams)



