from flask import request
from app.libs.redprint import Redprint
from app.models.base import db
from app.libs.error_code import Success
from app.models.player import Player

api = Redprint('player')

@api.route('/input_player',methods= ['POST'])
def input_player():
    data = request.get_json()
    with db.auto_commit():
        player = Player()
        player.player_name = data["player_name"]
        player.player_sex = data["player_sex"]
        player.player_picture = data["player_picture"]
        player.player_place = data["player_place"]
        player.team_id = data["team_id"]
        player.player_age = data["player_age"]
        player.player_number = data["player_number"]
        player.player_height = data["player_height"]
        player.player_weight = data["player_weight"]
        player.player_grade = data["player_grade"]
        player.school_id = data["school_id"]
        db.session.add(player)
    return Success(msg='新增成功')

@api.route('/alter_player',methods= ['POST'])
def alter_player():
    data = request.get_json()
    with db.auto_commit():
        players = Player.query.filter(Player.player_id == data["player_id"]).first()
        players.player_name  = data["player_name"]
        players.player_sex  = data["player_sex"]
        players.player_picture = data["player_picture"]
        players.player_place = data["player_place"]
        players.team_id = data["team_id"]
        players.player_age = data["player_age"]
        players.player_number = data["player_number"]
        players.player_height = data["player_height"]
        players.player_weight = data["player_weight"]
        players.player_grade = data["player_grade"]
        return Success(msg='修改成功')

@api.route('/select_id')
def select_id():
    data = request.args.get("team_id")
    player_message= Player.query.filter(Player.team_id == data).all()
    player_messages = []
    for me in player_message:
        player_messages.append(me.to_json())
    return Success(msg='查找成功',data=player_messages)

@api.route('/select')
def select():
    player = Player.query.all()
    players= []
    for man in player:
        players.append(man.to_json())
    return Success(msg='查找成功',data=players)

