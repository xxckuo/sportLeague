from flask import  request,jsonify
from sqlalchemy import desc

from app.libs.redprint import Redprint
from app.models.base import db
from app.libs.error_code import Success
from app.models.player import Player
from app.models.player_statistics import Player_statistics
from app.models.team import Team

api = Redprint('play_statistics')

@api.route('/create', methods=['POST'])
def play_statistics_create():
    jsonData = request.get_json()
    with db.auto_commit():
        play_statistics = Player_statistics()

        play_statistics.player_id = jsonData['player_id']
        play_statistics.league_id = jsonData['league_id']
        play_statistics.team_name= jsonData['team_name']
        play_statistics.pt_score = jsonData['pt_score']
        play_statistics.pt_assist = jsonData['pt_assist']
        play_statistics.pt_foul = jsonData['pt_foul']
        play_statistics.pt_yellow_card = jsonData['pt_yellow_card']
        play_statistics.pt_red_card = jsonData['pt_red_card']

        db.session.add(play_statistics)
    return Success(msg='新增球员积分榜成功')

@api.route('/select',methods = ['POST'])
def play_select():
    jsonData = request.get_json()
    plays = []

    if int(jsonData['select']) == 1:
        # play = Player_statistics.query.order_by(desc(Player_statistics.pt_score)).all()
        play = db.session.query(Player_statistics.player_id,Player.player_name,Player_statistics.pt_id,Player_statistics.team_name,
                                Player_statistics.pt_score,Player_statistics.pt_assist,Player_statistics.pt_foul,
                                Player_statistics.pt_yellow_card,Player_statistics.pt_red_card,Player.player_number).\
            filter(Player_statistics.pt_score!=0,Player_statistics.player_id == Player.player_id,Player_statistics.league_id == jsonData['league_id']).\
            order_by(Player_statistics.pt_score.desc()).all()
        params = 'pt_score'
    if int(jsonData['select']) == 2:
        play = db.session.query(Player_statistics.player_id, Player.player_name,Player_statistics.pt_id,
                                Player_statistics.team_name, Player_statistics.pt_score, Player_statistics.pt_assist,
                                Player_statistics.pt_foul, Player_statistics.pt_yellow_card,
                                Player_statistics.pt_red_card,Player.player_number). \
            filter(Player_statistics.pt_assist!=0,Player_statistics.player_id == Player.player_id,
                   Player_statistics.league_id == jsonData['league_id']). \
            order_by(Player_statistics.pt_assist.desc()).all()
        params = 'pt_assist'
    if int(jsonData['select']) == 3:
        play = db.session.query(Player_statistics.player_id, Player.player_name,Player_statistics.pt_id,
                                Player_statistics.team_name, Player_statistics.pt_score, Player_statistics.pt_assist,
                                Player_statistics.pt_foul, Player_statistics.pt_yellow_card,
                                Player_statistics.pt_red_card,Player.player_number). \
            filter(Player_statistics.pt_foul!=0,Player_statistics.player_id == Player.player_id,
                   Player_statistics.league_id == jsonData['league_id']). \
            order_by(Player_statistics.pt_foul.desc()).all()
        params = 'pt_foul'
    if int(jsonData['select']) == 4:
        play = db.session.query(Player_statistics.player_id, Player.player_name, Player_statistics.pt_id,
                                Player_statistics.team_name, Player_statistics.pt_score, Player_statistics.pt_assist,
                                Player_statistics.pt_foul, Player_statistics.pt_yellow_card,
                                Player_statistics.pt_red_card,Player.player_number). \
            filter(Player_statistics.pt_yellow_card!=0,Player_statistics.player_id == Player.player_id,
                   Player_statistics.league_id == jsonData['league_id']). \
            order_by(Player_statistics.pt_yellow_card.desc()).all()
        params = 'pt_yellow_card'
    if int(jsonData['select']) == 5:
        play = db.session.query(Player_statistics.player_id, Player.player_name,Player_statistics.pt_id,
                                Player_statistics.team_name, Player_statistics.pt_score, Player_statistics.pt_assist,
                                Player_statistics.pt_foul, Player_statistics.pt_yellow_card,
                                Player_statistics.pt_red_card,Player.player_number). \
            filter(Player_statistics.pt_red_card!=0,Player_statistics.player_id == Player.player_id,
                   Player_statistics.league_id == jsonData['league_id']). \
            order_by(Player_statistics.pt_red_card.desc()).all()
        params = 'pt_red_card'

    for p in range(len(play)):

        player = {}

        player['player_id'] = play[p][0]
        player['player_name'] = play[p][1]
        player['pt_id'] = play[p][2]
        player['team_name'] = play[p][3]
        player['pt_score'] = play[p][4]
        player['pt_assist'] = play[p][5]
        player['pt_foul'] = play[p][6]
        player['pt_yellow_card'] = play[p][7]
        player['pt_red_card'] = play[p][8]
        player['player_number'] = play[p][9]
        player['rank'] =p
        # 判断是否是第一个，如果是直接赋值为1
        # 如果不是第一个，与上面的进行对比，对比结果分析，
        # 如果和上面的值大小一样，直接使用上面的排名进行赋值，
        # 如果比上一个小，则使用它在列表中的顺序+1

        if p==0:
            player['rank'] = 1
        else:
            if player[params]<plays[p-1][params]:
                player['rank'] = p + 1
            else:
                player['rank']=plays[p-1]['rank']

        plays.append(player)
    return Success(msg='查找球员积分榜成功', data=plays)


