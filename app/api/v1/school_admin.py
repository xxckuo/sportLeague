from flask import request

from app.libs.error_code import Success
from app.libs.redprint import Redprint
from app.models.base import db
from app.models.school_admin import School_admin

api = Redprint('school_admin')

@api.route('/create',methods=['POST'])
def create_school_admin():
    jsonData = request.get_json()
    with db.auto_commit():
        school_admin = School_admin()
        school_admin.school_id = jsonData['school_id']
        school_admin.sa_auth = jsonData['sa_auth']
        school_admin.sa_account = jsonData['sa_account']
        school_admin.sa_name = jsonData['sa_name']
        school_admin.sa_password = jsonData['sa_password']
        db.session.add(school_admin)
    return Success(msg='新增管理员成功')

@api.route('/update',methods=['POST'])
def update_school_admin():
    jsonData = request.get_json()
    with db.auto_commit():
        sc = School_admin.query.filter(School_admin.sa_id == jsonData['sa_id']).first()
        sc.sa_name = jsonData['sa_name']
        # sc.school_id = jsonData['school_id']
        return Success(msg='修改管理员成功')

@api.route('/delete')
def delete_school_admin():
    schooladmin_id = request.args.get('schooladmin_id')
    # print(schooladmin_id)
    with db.auto_commit():
        sa = School_admin.query.filter_by(sa_id=schooladmin_id).first()
        sa.status = 0
        # db.session.delete(sc)
        return Success(msg='删除管理员成功')

@api.route('/get', methods=['GET'])
def get_school_admin():

    school_id = request.args.get('school_id')

    school_admin = School_admin.query.filter_by(school_id = school_id)

    schools = []
    for sc in school_admin:
        schools.append(sc.to_json())
    return Success(msg='查找管理员成功',data=schools)