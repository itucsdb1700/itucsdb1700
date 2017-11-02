from flask import render_template
from flask import current_app
from flask import request
from classes.game_friends_class import GameAnnounce

import psycopg2 as dbapi2


def game_friend_page():
    if request.method == 'POST':
        gameName = request.form['InputGameName']
        gameType = request.form['InputGameType']
        if not request.form['GamePlayerNo']:
            playerNum = None
        else:
            playerNum = int(request.form['GamePlayerNo'])
        gameDate = request.form['InputGameDate']
        gameLoc = request.form['InputGameLocation']
        gameDesc = request.form['GameDescription']

        gameAnnounce = GameAnnounce(gameName,gameType,playerNum,gameDate,gameLoc,gameDesc)

        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()

            query = """INSERT INTO GAMEFRIEND (NAME, TYPE, GAMEDATE, LOCATION, PLAYERNUMBER, DESCRIPTION) 
                                                VALUES('%s', '%s', '%s', '%s', '%d', '%s')""" % (
                gameAnnounce.gameName, gameAnnounce.gameType, gameAnnounce.gameDate,
                gameAnnounce.gameLoc, gameAnnounce.playerNum, gameAnnounce.gameDesc)

            cursor.execute(query)
            connection.commit()

        return render_template('game_friends.html')

    else:
        return render_template('game_friends.html')
