from flask import render_template
from flask import current_app
from flask import request
from flask_login import current_user
from flask import session

from flask import redirect
from flask.helpers import url_for

from classes.game_friends_class import GameAnnounce

import psycopg2 as dbapi2


def game_friend_page():
    if request.method == 'POST':
        if 'userSearchButton' in request.form:  # if the search button is submitted
            session['search_username'] = request.form['usernameSearch']
            return redirect(url_for('site.SearchUserPage'))

        # current user information is taken
        username = current_user.get_username()
        email = current_user.get_email()
        # name = current_user.get_name()
        # surname = current_user.get_surname()

        gameName = request.form['InputGameName']
        gameType = request.form['InputGameType']
        if not request.form['GamePlayerNo']:
            playerNum = None
        else:
            playerNum = int(request.form['GamePlayerNo'])
        gameDate = request.form['InputGameDate']
        gameLoc = request.form['InputGameLocation']
        gameDesc = request.form['GameDescription']

        with dbapi2.connect(current_app.config['dsn']) as connection:
            # to take the current user's name and email
            cursor1 = connection.cursor()
            statement = """SELECT ID FROM USERS WHERE (USERS.USERNAME = %s) AND (USERS.EMAIL = %s)"""
            cursor1.execute(statement, (username, email))
            UserId = cursor1.fetchone()
            UserId = UserId[0]

            gameAnnounce = GameAnnounce(gameName, gameType, playerNum, gameDate, gameLoc, gameDesc, UserId)
            # print(type(UserId))

            # to insert the new announcement information
            cursor = connection.cursor()
            query = """INSERT INTO GAMEFRIEND (NAME, TYPE, GAMEDATE, LOCATION, PLAYERNUMBER, DESCRIPTION, USERID) 
                                                VALUES(%s,%s,%s,%s,%s,%s,%s)"""
            cursor.execute(query, (gameAnnounce.gameName, gameAnnounce.gameType,
                                   gameAnnounce.gameDate, gameAnnounce.gameLoc,
                                   gameAnnounce.playerNum, gameAnnounce.gameDesc, gameAnnounce.user_id))
            connection.commit()

        #return render_template('game_friends.html')
        return redirect(url_for('site.GameFriendPage'))

    else:
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """SELECT GAMEFRIEND.NAME, TYPE, GAMEDATE, LOCATION, PLAYERNUMBER, DESCRIPTION, 
            USERS.NAME, USERS.SURNAME, USERS.EMAIL, FACULTIES.FACULTYNAME, FACULTIES.FACULTYCODE 
            FROM GAMEFRIEND, USERS, FACULTIES 
            WHERE (GAMEFRIEND.USERID = USERS.ID) AND (USERS.FACULTYID = FACULTIES.ID)"""
            cursor.execute(query)
            gameFriendAnnounces = cursor.fetchall()

        return render_template('game_friends.html', gameFriendAnnounces=gameFriendAnnounces)
