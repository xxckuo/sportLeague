from flask import Blueprint
from app.api.v1 import school_admin,school,category


def create_blueprint_v1():
    bp_v1 = Blueprint('v1', __name__)
    school_admin.api.register(bp_v1)
    school.api.register(bp_v1)
    category.api.register(bp_v1)

    return bp_v1