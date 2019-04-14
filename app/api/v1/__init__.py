from flask import Blueprint
from app.api.v1 import school, school_admin, league, group, grade, turns, schedule, team, player, \
    play_statistics, category


def create_blueprint_v1():
    bp_v1 = Blueprint('v1', __name__)
    school.api.register(bp_v1)
    school_admin.api.register(bp_v1)
    league.api.register(bp_v1)
    grade.api.register(bp_v1)
    group.api.register(bp_v1)
    turns.api.register(bp_v1)
    schedule.api.register(bp_v1)
    team.api.register(bp_v1)
    category.api.register(bp_v1)
    player.api.register(bp_v1)
    play_statistics.api.register(bp_v1)
    return bp_v1