from flask import jsonify, request
from app.libs.redprint import Redprint
from app.models.base import db
from app.models.school import School
from app.libs.error_code import Success

api = Redprint('school')

@api.route('/get', methods=['GET'])
def get_school():
    school = School.query.all()
    schools = []
    for sc in school:
        schools.append(sc.to_json())
    return Success(msg='查找成功',data=schools)

@api.route('/create', methods=['POST'])
def create_school():
    jsonData = request.get_json()
    with db.auto_commit():
        school = School()
        school.school_name = jsonData['school_name']
        school.school_address = jsonData['school_address']
        db.session.add(school)
    return Success(msg='新增成功')

@api.route('/update')
def update_school():
    with db.auto_commit():
        sc = School.query.filter(School.school_name == "黑龙江科技大学7").first()
        sc.school_name = "黑龙江科技大学"
    return '修改成功'

@api.route('/delete')
def delete_school():
    data = request.args.get('school_name')
    with db.auto_commit():
        sc = School.query.filter(School.school_name == data).first()
        db.session.delete(sc)
    return '删除成功'