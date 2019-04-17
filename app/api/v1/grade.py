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
    data = db.session.query(Grade.grade_id,Grade.grade_team,Grade.grade_turns,Grade.grade_win,Grade.grade_equal
                                ,Grade.grade_lose,Grade.grade_goal,Grade.grade_fumble,Grade.grade_integral,Team.team_logo,Team.team_name,Team.team_id).filter(Grade.league_id == league_id,Team.team_id == Grade.grade_team).\
            order_by(Grade.grade_integral.desc())
    messages = []
    for t in data:
        d = {}
        d['grade_id']=t[0]
        d['grade_team'] = t[1]
        d['grade_turns'] = t[2]
        d['grade_win'] = t[3]
        d['grade_equal'] = t[4]
        d['grade_lose'] = t[5]
        d['grade_goal'] = t[6]
        d['grade_fumble'] = t[7]
        d['grade_integral'] = t[8]
        d['team_logo']=t[9]
        d['team_name']=t[10]
        d['team_id']=t[11]
        messages.append(d)
    return Success(msg='查询成功', data=messages)
