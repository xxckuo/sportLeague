from flask import Blueprint

from app.libs.redprint import Redprint

from app.models.school import School

api = Redprint('user')

@api.route('/get')
def get_user():
    return 'this is project'