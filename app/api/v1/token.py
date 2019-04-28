from flask import request,  jsonify, current_app

from app.libs.error_code import FailError, Success
from app.libs.redprint import Redprint
from app.models.school_admin import School_admin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

api = Redprint('token')

@api.route('/token_get', methods=['POST'])
def get_token():
    data = request.json
    user = School_admin.query.filter_by(sa_name=data['nickname']).first()
    if user and user.check_password(data['password']) :
        #生成令牌
        uid = user.sa_id
        sa_auth = user.sa_auth
        school_id = user.school_id
        admin_name = user.sa_name
        # tokens = generate_auth_token(uid,school_id,admin_name)

        # 过期时间
        expiration = current_app.config['TOKEN_EXPIRATION']
        token = generate_auth_token(uid,sa_auth,school_id,admin_name,expiration)
        t = {
            'token': token.decode('ascii')
        }
        # return Success(msg='登录成功',data = jsonify(t))
        return jsonify(t)
    else:
        return FailError(msg='账号或密码不正确')


def generate_auth_token(uid,sa_auth,school_id,admin_name,expiration=7200):

    # 生成令牌
    s = Serializer(current_app.config['SECRET_KEY'],
                  expires_in=expiration)
    return s.dumps({
        'uid':uid,
        'school_id':school_id,
        'admin_name':admin_name,
        'sa_auth':sa_auth
    })

