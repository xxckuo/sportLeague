from flask import Blueprint, g

from app.api.v1.token_auth import auth
from app.libs.error_code import Success
from app.libs.redprint import Redprint
from app.models.school_admin import School_admin

api = Redprint('user')

@api.route('/get',methods = ['GET'])
@auth.login_required
def get_user():
    # uid = g.user.uid
    # user = School_admin.query.filter_by(sa_id = uid).first()
    # print (user.school_id)
    sc = {'uid':g.user.uid,
        'school_id':g.user.school_id,
        'admin_name':g.user.admin_name,
        'sa_auth':g.user.sa_auth
          }

    schools = []

    schools.append(sc)
    return Success(msg='查找管理员成功', data=schools)
