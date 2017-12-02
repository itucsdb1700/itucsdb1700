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

        formtype = request.form['form-name']
        username = current_user.get_username()
        email = current_user.get_email()

        if formtype == "GameFriend":
            gameName = request.form['InputGameName']
            gameType = request.form['InputGameType']
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

            # return render_template('game_friends.html')
            return redirect(url_for('site.GameFriendPage'))

        elif formtype == "GameFriendUpdate":
            with dbapi2.connect(current_app.config['dsn']) as connection:
                cursor = connection.cursor()  # prevented sql injection
                statement = """SELECT ID FROM USERS WHERE (USERS.USERNAME = %s) AND (USERS.EMAIL = %s)"""
                cursor.execute(statement, (username, email))
                announce_user_id = cursor.fetchone()
                announceid = request.form['announce-id']

                gameName = request.form['InputGameName']
                if not gameName:
                    statement = """SELECT NAME FROM GAMEFRIEND WHERE GAMEFRIEND.ID = %s"""
                    cursor.execute(statement, announceid)
                    gameName = cursor.fetchone()

                gameType = request.form['InputGameType']
                if not gameType:
                    statement = """SELECT TYPE FROM GAMEFRIEND WHERE GAMEFRIEND.ID = %s"""
                    cursor.execute(statement, announceid)
                    gameType = cursor.fetchone()

                playerNum = request.form['GamePlayerNo']
                if not playerNum:
                    statement = """SELECT PLAYERNUMBER FROM GAMEFRIEND WHERE GAMEFRIEND.ID = %s"""
                    cursor.execute(statement, announceid)
                    playerNum = cursor.fetchone()

                gameDate = request.form['InputGameDate']
                if not gameDate:
                    statement = """SELECT GAMEDATE FROM GAMEFRIEND WHERE GAMEFRIEND.ID = %s"""
                    cursor.execute(statement, announceid)
                    gameDate = cursor.fetchone()

                gameLoc = request.form['InputGameLocation']
                if not gameLoc:
                    statement = """SELECT LOCATION FROM GAMEFRIEND WHERE GAMEFRIEND.ID = %s"""
                    cursor.execute(statement, announceid)
                    gameLoc = cursor.fetchone()

                gameDesc = request.form['GameDescription']
                if not gameDesc:
                    statement = """SELECT DESCRIPTION FROM GAMEFRIEND WHERE GAMEFRIEND.ID = %s"""
                    cursor.execute(statement, announceid)
                    gameDesc = cursor.fetchone()

                print(playerNum)

                statement = """UPDATE GAMEFRIEND SET NAME = %s, TYPE = %s, PLAYERNUMBER = %s, GAMEDATE = %s, LOCATION = %s, DESCRIPTION = %s, USERID = %s WHERE GAMEFRIEND.ID = %s"""
                cursor.execute(statement,
                               (gameName, gameType, playerNum, gameDate, gameLoc, gameDesc, announce_user_id, announceid))
                connection.commit()
                return redirect(url_for('site.SelectedGameAnnounce', announceId=announceid))

    else:
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """SELECT GAMEFRIEND.NAME, TYPE, GAMEDATE, LOCATION, PLAYERNUMBER, DESCRIPTION, 
            USERS.NAME, USERS.SURNAME, USERS.EMAIL, FACULTIES.FACULTYNAME, FACULTIES.FACULTYCODE, USERS.USERNAME, GAMEFRIEND.ID
            FROM GAMEFRIEND, USERS, FACULTIES 
            WHERE (GAMEFRIEND.USERID = USERS.ID) AND (USERS.FACULTYID = FACULTIES.ID)"""
            cursor.execute(query)
            gameFriendAnnounces = cursor.fetchall()

        return render_template('game_friends.html', gameFriendAnnounces=gameFriendAnnounces)
