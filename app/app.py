from flask import Flask
from app.api.v1 import create_blueprint_v1
from app.models.base import db
from app.models.category import Category
from app.models.grade import Grade
from app.models.group import Group
from app.models.group_team import Group_team
from app.models.league import League
from app.models.player import Player
from app.models.schedule import Schedule
from app.models.school import School
from app.models.school_admin import School_admin
from app.models.team import Team
from app.models.turns import Turns
from app.models.player_statistics import Player_statistics


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.secure')
    app.config.from_object('app.config.setting')
    app.register_blueprint(create_blueprint_v1(), url_prefix='/v1')

    db.init_app(app)
    with app.app_context():
        db.create_all(app=app)

    return app
