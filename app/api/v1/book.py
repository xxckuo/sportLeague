from flask import Blueprint,jsonify

from app.libs.redprint import Redprint






api = Redprint('book')

@api.route('/get')
def get_book():
    dictDemo={
        0:{"tom":"90","jerry":"75"},
        1:{"tom":"90","jerry":"75"}
    }
    return jsonify(dictDemo)

@api.route('/create')
def create_book():
    return 'create book'