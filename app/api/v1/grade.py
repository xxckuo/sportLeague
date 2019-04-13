from flask import jsonify, request
from app.libs.redprint import Redprint
from app.models.base import db
from app.libs.error_code import Success
from app.models.grade import Grade
from app.models.league import League

api = Redprint('grade')

@api.route('/create_grade', methods=['POST'])
def create_grade():
    jsonData = request.get_json()
    print(jsonData)
    with db.auto_commit():
        grade = Grade()
        league_message = League.query.filter(League.league_id==jsonData['league_id']).all()
        league_messages = []
        for me in league_message:
            league_messages.append(me.to_json())
            print(league_messages)
            if league_messages[0]['league_type'] == 1:
                grade.grade_team = jsonData['grade_team']
                grade.grade_turns =0 #jsonData['grade_turns']
                grade.grade_win = 0 #jsonData['grade_win']
                grade.grade_equal = 0 #jsonData['grade_equal']
                grade.grade_lose = 0 #jsonData['grade_lose']
                grade.grade_goal = 0 #jsonData['grade_goal']
                grade.grade_fumble = 0 #jsonData['grade_fumble']
                grade.grade_integral = 0  #jsonData['grade_integral']
                db.session.add(grade)
            return Success(msg='新增成功')



    #     print(league_message)
    #     if league_message["league_type"] == 1:
    #         grade.grade_name = jsonData['grade_name']
    #         grade.grade_turns =0 #jsonData['grade_turns']
    #         grade.grade_win = 0 #jsonData['grade_win']
    #         grade.grade_equal = 0 #jsonData['grade_equal']
    #         grade.grade_lose = 0 #jsonData['grade_lose']
    #         grade.grade_goal = 0 #jsonData['grade_goal']
    #         grade.grade_fumble = 0 #jsonData['grade_fumble']
    #         grade.grade_integral = 0  #jsonData['grade_integral']
    #         db.session.add(grade)
    # return Success(msg='新增成功')