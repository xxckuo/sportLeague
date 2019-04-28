import json
from flask_httpauth import HTTPBasicAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer,BadSignature,SignatureExpired
from flask import current_app, g
from sqlalchemy.util import namedtuple

from app.libs.error_code import AuthFailed, Success


auth = HTTPBasicAuth()
User = namedtuple('User',['uid','school_id','admin_name','sa_auth'])




# 验证token
@auth.verify_password
# 拿到了token
def verify_password(token,password):

    # 调用verify_auth_token
    user_info = verify_auth_token(token)
    # print(user_info)
    if not user_info:
        return False
    else:
        g.user = user_info
        return True
        # data = json.dumps(user_info)
        # print(data)
        # return Success(msg='查找管理员成功', data=data)

# 验证token将token解码
def verify_auth_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except BadSignature:
        raise AuthFailed(msg = 'token错误')
    except SignatureExpired:
        raise AuthFailed(msg = 'token已过时')
    uid = data['uid']
    school_id = data['school_id']
    admin_name = data['admin_name']
    sa_auth = data['sa_auth']
    return User(uid,school_id,admin_name,sa_auth)
    # return{
    #     'uid':uid,
    #     'school_id':school_id,
    #     'admin_name':admin_name,
    #     'sa_auth':sa_auth
    # }