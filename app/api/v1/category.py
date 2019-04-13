from flask import jsonify, request
from app.libs.redprint import Redprint
from app.models.base import db
from app.models.category import Category
from app.libs.error_code import Success

api = Redprint('category')

@api.route('/create', methods=['POST'])
def create_category():
    jsonData = request.get_json()
    with db.auto_commit():
        category = Category()
        category.category_name = jsonData['category_name']
        db.session.add(category)
    return Success(msg='新增赛事类型成功')

@api.route('/delete')
def delete_category():
    category_id = request.args.get('category_id')

    with db.auto_commit():
        category = Category.query.filter_by(category_id=category_id).first()
        category.status = 0
        # db.session.delete(sc)
    return Success(msg='删除赛事类型成功')

@api.route('/update',methods=['POST'])
def category_school():
    jsonData = request.get_json()
    with db.auto_commit():
        category = Category.query.filter(Category.category_id == jsonData['category_id']).first()
        category.category_name = jsonData['category_name']
        return Success(msg='修改赛事类型成功')

@api.route('/get', methods=['GET'])
def get_category():
    category = Category.query.filter_by()
    categorys = []
    for sc in category:
        categorys.append(sc.to_json())
    return Success(msg='查找赛事类型成功',data=categorys)