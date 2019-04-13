from flask import jsonify, request
from app.libs.redprint import Redprint
from app.models.base import db
from app.models.school import School
from app.libs.error_code import Success

api = Redprint('school')

@api.route('/get', methods=['GET'])
def get_school():
    school = School.query.filter_by()
    schools = []
    for sc in school:
        schools.append(sc.to_json())
    return Success(msg='查找学校成功',data=schools)

@api.route('/create', methods=['POST'])
def create_school():
    jsonData = request.get_json()
    with db.auto_commit():
        school = School()
        school.school_name = jsonData['school_name']
        school.school_address = jsonData['school_address']
        db.session.add(school)
    return Success(msg='新增学校成功')

@api.route('/update',methods=['POST'])
def update_school():
    jsonData = request.get_json()
    with db.auto_commit():
        sc = School.query.filter(School.school_id == jsonData['school_id']).first()
        sc.school_name = jsonData['school_name']
        sc.school_address = jsonData['school_address']
        return Success(msg='修改学校成功')

@api.route('/delete')
def delete_school():
    school_id = request.args.get('school_id')
    # print(school_id)
    with db.auto_commit():
        sc = School.query.filter_by(school_id=school_id).first()
        sc.status = 0
        # db.session.delete(sc)
    return Success(msg='删除学校成功')