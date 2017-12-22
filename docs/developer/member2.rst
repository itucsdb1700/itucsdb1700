Parts Implemented by Görkem Toppeker
====================================

Game Friend Finding page is related to GAMEANNOUNCE table.

ITU Activities page is related to ITUACTIVITIES table.

Club Activities page is related to CLUBACTIVITIES table.

Sport Activities page is related to SPORTACTIVITIES table.


Game Friend Finding Page
------------------------

The operations for Game Friend Finding page is done using the class: GameAnnounce

.. code-block:: python

	class GameAnnounce:
		def __init__(self, gameName, gameType, playerNum, gameDate, gameLoc, gameDesc, user_id):
			self.gameName = gameName
			self.gameType = gameType
			self.playerNum = playerNum
			self.gameDate = gameDate
			self.gameLoc = gameLoc
			self.gameDesc = gameDesc
			self.user_id = user_id
			
			
Users can add new Game Announces to the database by modal form. The below code is responsible of taking information from modal form.

.. code-block:: python

		gameName = request.form['InputGameName']
		gameType = request.form['InputGameType']
		playerNum = int(request.form['GamePlayerNo'])
		gameDate = request.form['InputGameDate']
		gameLoc = request.form['InputGameLocation']
		gameDesc = request.form['GameDescription']

The user id of the poster of the game announce is taken, then an object of that class is created. After that, this entry is added to database by below code.

.. code-block:: python

    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor1 = connection.cursor()
        statement = """SELECT ID FROM USERS WHERE (USERS.USERNAME = %s) AND (USERS.EMAIL = %s)"""
        cursor1.execute(statement, (username, email))
        UserId = cursor1.fetchone()
        UserId = UserId[0]

        gameAnnounce = GameAnnounce(gameName, gameType, playerNum, gameDate, gameLoc, gameDesc, UserId)

        cursor = connection.cursor()
        query = """INSERT INTO GAMEANNOUNCE (NAME, TYPE, GAMEDATE, LOCATION, PLAYERNUMBER, DESCRIPTION, USERID)
                    VALUES(%s,%s,%s,%s,%s,%s,%s)"""
        cursor.execute(query, (gameAnnounce.gameName, gameAnnounce.gameType,
        gameAnnounce.gameDate, gameAnnounce.gameLoc,
        gameAnnounce.playerNum, gameAnnounce.gameDesc, gameAnnounce.user_id))
        connection.commit()

Users can update existing Game Announce records. Below code is used for update operation.

.. code-block:: python

    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()  # prevented sql injection
        statement = """SELECT ID FROM USERS WHERE (USERS.USERNAME = %s) AND (USERS.EMAIL = %s)"""
        cursor.execute(statement, (username, email))
        announce_user_id = cursor.fetchone()
        announceid = request.form['announce-id']

        gameName = request.form['InputGameName']
        if not gameName:
            statement = """SELECT NAME FROM GAMEANNOUNCE WHERE GAMEANNOUNCE.ID = %s"""
            cursor.execute(statement, announceid)
            gameName = cursor.fetchone()

            playerNum = request.form['GamePlayerNo']
                if not playerNum:
                    statement = """SELECT PLAYERNUMBER FROM GAMEANNOUNCE WHERE GAMEANNOUNCE.ID = %s"""
                    cursor.execute(statement, announceid)
                    playerNum = cursor.fetchone()

            gameDate = request.form['InputGameDate']
                if not gameDate:
                    statement = """SELECT GAMEDATE FROM GAMEANNOUNCE WHERE GAMEANNOUNCE.ID = %s"""
                    cursor.execute(statement, announceid)
                    gameDate = cursor.fetchone()

            gameLoc = request.form['InputGameLocation']
                if not gameLoc:
                    statement = """SELECT LOCATION FROM GAMEANNOUNCE WHERE GAMEANNOUNCE.ID = %s"""
                    cursor.execute(statement, announceid)
                    gameLoc = cursor.fetchone()

            gameDesc = request.form['GameDescription']
                if not gameDesc:
                    statement = """SELECT DESCRIPTION FROM GAMEANNOUNCE WHERE GAMEANNOUNCE.ID = %s"""
                    cursor.execute(statement, announceid)
                    gameDesc = cursor.fetchone()

The below code updates the existing record via using this query.

.. code-block:: python

    statement = """UPDATE GAMEANNOUNCE SET NAME = %s, PLAYERNUMBER = %s, GAMEDATE = %s, LOCATION = %s, DESCRIPTION = %s, USERID = %s WHERE GAMEANNOUNCE.ID = %s"""
    cursor.execute(statement,
        (gameName, playerNum, gameDate, gameLoc, gameDesc, announce_user_id, announceid))
    connection.commit()



.. raw:: latex

    \newpage

ITU Activities Page
-------------------

The operations for ITU Activities Page is done using the class: ItuActivity

.. code-block:: python

    class ItuActivity:
        def __init__(self, activityName, participantName, activityDate, activityTime, activityLoc, activityDesc ,user_id):
            self.activityName = activityName
            self.participantName = participantName
            self.activityDate = activityDate
            self.activityTime = activityTime
            self.activityLoc = activityLoc
            self.activityDesc = activityDesc
            self.user_id = user_id


Users can add new ITU Activities to the database by modal form. The below code is responsible of taking information from modal form.

.. code-block:: python

    activityName = request.form['InputActivityName']
    participantName = request.form['InputParticipantName']
    activityDate = request.form['InputActivityDate']
    activityTime = request.form['InputActivityTime']
    activityLoc = request.form['InputActivityLocation']
    activityDesc = request.form['ActivityDescription']

The user id of the poster of the activity announce is taken, then an object of that class is created. After that, this entry is added to database by below code.

.. code-block:: python

    with dbapi2.connect(current_app.config['dsn']) as connection:

        cursor1 = connection.cursor()
        statement = """SELECT ID FROM USERS WHERE (USERS.USERNAME = %s) AND (USERS.EMAIL = %s)"""
        cursor1.execute(statement, (username, email))
        UserId = cursor1.fetchone()
        UserId = UserId[0]

        ituActivity = ItuActivity(activityName, participantName, activityDate, activityTime, activityLoc,
            activityDesc, UserId)

        cursor = connection.cursor()
        query = """INSERT INTO ITUACTIVITIES (NAME, SPECIALPARTICIPANT, ACTIVITYDATE, ACTIVITYTIME, LOCATION, DESCRIPTION, USERID)
            VALUES(%s,%s,%s,%s,%s,%s,%s)"""
        cursor.execute(query, (ituActivity.activityName, ituActivity.participantName,
            ituActivity.activityDate, ituActivity.activityTime, ituActivity.activityLoc, ituActivity.activityDesc, ituActivity.user_id))
        connection.commit()

Users can update existing ITU Activity records. Below code is used for update operation.

.. code-block:: python

    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()  # prevented sql injection
        statement = """SELECT ID FROM USERS WHERE (USERS.USERNAME = %s) AND (USERS.EMAIL = %s)"""
        cursor.execute(statement, (username, email))
        activity_user_id = cursor.fetchone()
        activityid = request.form['activity-id']

        activityName = request.form['InputActivityName']
        if not activityName:
            statement = """SELECT NAME FROM ITUACTIVITIES WHERE ITUACTIVITIES.ID = %s"""
            cursor.execute(statement, activityid)
            activityName = cursor.fetchone()

        participantName = request.form['InputParticipantName']
        if not participantName:
            statement = """SELECT SPECIALPARTICIPANT FROM ITUACTIVITIES WHERE ITUACTIVITIES.ID = %s"""
            cursor.execute(statement, activityid)
            participantName = cursor.fetchone()

        activityDate = request.form['InputActivityDate']
        if not activityDate:
            statement = """SELECT ACTIVITYDATE FROM ITUACTIVITIES WHERE ITUACTIVITIES.ID = %s"""
            cursor.execute(statement, activityid)
            activityDate = cursor.fetchone()

        activityTime = request.form['InputActivityTime']
        if not activityTime:
            statement = """SELECT ACTIVITYTIME FROM ITUACTIVITIES WHERE ITUACTIVITIES.ID = %s"""
            cursor.execute(statement, activityid)
            activityTime = cursor.fetchone()

        activityLoc = request.form['InputActivityLocation']
        if not activityLoc:
            statement = """SELECT LOCATION FROM ITUACTIVITIES WHERE ITUACTIVITIES.ID = %s"""
            cursor.execute(statement, activityid)
            activityLoc = cursor.fetchone()

        activityDesc = request.form['ActivityDescription']
        if not activityDesc:
            statement = """SELECT DESCRIPTION FROM ITUACTIVITIES WHERE ITUACTIVITIES.ID = %s"""
            cursor.execute(statement, activityid)
            activityDesc = cursor.fetchone()

The below code updates the existing record via using this query.

.. code-block:: python

    statement = """UPDATE ITUACTIVITIES SET NAME = %s, SPECIALPARTICIPANT = %s, ACTIVITYDATE = %s, ACTIVITYTIME = %s, LOCATION = %s, DESCRIPTION = %s, USERID = %s WHERE ITUACTIVITIES.ID = %s"""
                cursor.execute(statement,
                               (activityName, participantName, activityDate, activityTime, activityLoc, activityDesc, activity_user_id, activityid))
                connection.commit()



.. raw:: latex

    \newpage


Club Activities Page
--------------------

The operations for Club Activities Page is done using the class: ClubActivity

.. code-block:: python

    class ClubActivity:
        def __init__(self, activityName, clubName, activityDate, activityTime, activityLoc, activityDesc, user_id):
            self.activityName = activityName
            self.clubName = clubName
            self.activityDate = activityDate
            self.activityTime = activityTime
            self.activityLoc = activityLoc
            self.activityDesc = activityDesc
            self.user_id = user_id


Users can add new Club Activities to the database by modal form. The below code is responsible of taking information from modal form.

.. code-block:: python

    activityName = request.form['InputActivityName']
    clubName = request.form['InputClubName']
    activityDate = request.form['InputActivityDate']
    activityTime = request.form['InputActivityTime']
    activityLoc = request.form['InputActivityLocation']
    activityDesc = request.form['ActivityDescription']

The user id of the poster of the activity announce is taken, then an object of that class is created. After that, this entry is added to database by below code.

.. code-block:: python

    with dbapi2.connect(current_app.config['dsn']) as connection:

        cursor1 = connection.cursor()
        statement = """SELECT ID FROM USERS WHERE (USERS.USERNAME = %s) AND (USERS.EMAIL = %s)"""
        cursor1.execute(statement, (username, email))
        UserId = cursor1.fetchone()
        UserId = UserId[0]

        clubActivity = ClubActivity(activityName, clubName, activityDate, activityTime, activityLoc,
            activityDesc, UserId)

        cursor = connection.cursor()
        query = """INSERT INTO CLUBACTIVITIES (NAME, CLUBNAME, ACTIVITYDATE, ACTIVITYTIME, LOCATION, DESCRIPTION, USERID)
            VALUES(%s,%s,%s,%s,%s,%s,%s)"""
        cursor.execute(query, (clubActivity.activityName, clubActivity.clubName,
        clubActivity.activityDate, clubActivity.activityTime,
        clubActivity.activityLoc, clubActivity.activityDesc, clubActivity.user_id))
        connection.commit()

Users can update existing Club Activity records. Below code is used for update operation.

.. code-block:: python

    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()  # prevented sql injection
        statement = """SELECT ID FROM USERS WHERE (USERS.USERNAME = %s) AND (USERS.EMAIL = %s)"""
        cursor.execute(statement, (username, email))
        activity_user_id = cursor.fetchone()
        activityid = request.form['activity-id']

        activityName = request.form['InputActivityName']
        if not activityName:
            statement = """SELECT NAME FROM CLUBACTIVITIES WHERE CLUBACTIVITIES.ID = %s"""
            cursor.execute(statement, activityid)
            activityName = cursor.fetchone()

        clubName = request.form['InputClubName']
        if not clubName:
            statement = """SELECT CLUBNAME FROM CLUBACTIVITIES WHERE CLUBACTIVITIES.ID = %s"""
            cursor.execute(statement, activityid)
            clubName = cursor.fetchone()

        activityDate = request.form['InputActivityDate']
        if not activityDate:
            statement = """SELECT ACTIVITYDATE FROM CLUBACTIVITIES WHERE CLUBACTIVITIES.ID = %s"""
            cursor.execute(statement, activityid)
            activityDate = cursor.fetchone()

        activityTime = request.form['InputActivityTime']
        if not activityTime:
            statement = """SELECT ACTIVITYTIME FROM CLUBACTIVITIES WHERE CLUBACTIVITIES.ID = %s"""
            cursor.execute(statement, activityid)
            activityTime = cursor.fetchone()

        activityLoc = request.form['InputActivityLocation']
        if not activityLoc:
            statement = """SELECT LOCATION FROM CLUBACTIVITIES WHERE CLUBACTIVITIES.ID = %s"""
            cursor.execute(statement, activityid)
            activityLoc = cursor.fetchone()

        activityDesc = request.form['ActivityDescription']
        if not activityDesc:
            statement = """SELECT DESCRIPTION FROM CLUBACTIVITIES WHERE CLUBACTIVITIES.ID = %s"""
            cursor.execute(statement, activityid)
            activityDesc = cursor.fetchone()

The below code updates the existing record via using this query.

.. code-block:: python

    statement = """UPDATE CLUBACTIVITIES SET NAME = %s, CLUBNAME = %s, ACTIVITYDATE = %s, ACTIVITYTIME = %s, LOCATION = %s, DESCRIPTION = %s, USERID = %s WHERE CLUBACTIVITIES.ID = %s"""
    cursor.execute(statement,
        (activityName, clubName, activityDate, activityTime, activityLoc, activityDesc, activity_user_id, activityid))
    connection.commit()



Sport Activities Page
---------------------

The operations for Sport Activities Page is done using the class: SportActivity

.. code-block:: python

    class SportActivity:
        def __init__(self, activityName, sportName, activityDate, activityTime, activityLoc, activityDesc, user_id):
            self.activityName = activityName
            self.sportName = sportName
            self.activityDate = activityDate
            self.activityTime = activityTime
            self.activityLoc = activityLoc
            self.activityDesc = activityDesc
            self.user_id = user_id


Users can add new Sport Activities to the database by modal form. The below code is responsible of taking information from modal form.

.. code-block:: python

    activityName = request.form['InputActivityName']
    sportName = request.form['InputSportName']
    activityDate = request.form['InputActivityDate']
    activityTime = request.form['InputActivityTime']
    activityLoc = request.form['InputActivityLocation']
    activityDesc = request.form['ActivityDescription']

The user id of the poster of the activity announce is taken, then an object of that class is created. After that, this entry is added to database by below code.

.. code-block:: python

    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor1 = connection.cursor()
        statement = """SELECT ID FROM USERS WHERE (USERS.USERNAME = %s) AND (USERS.EMAIL = %s)"""
        cursor1.execute(statement, (username, email))
        UserId = cursor1.fetchone()
        UserId = UserId[0]

        sportActivity = SportActivity(activityName, sportName, activityDate, activityTime, activityLoc,
            activityDesc, UserId)

        cursor = connection.cursor()
        query = """INSERT INTO SPORTACTIVITIES (NAME, SPORTNAME, ACTIVITYDATE, ACTIVITYTIME, LOCATION, DESCRIPTION, USERID)
            VALUES(%s,%s,%s,%s,%s,%s,%s)"""
        cursor.execute(query, (sportActivity.activityName, sportActivity.sportName,
            sportActivity.activityDate, sportActivity.activityTime, sportActivity.activityLoc, sportActivity.activityDesc, sportActivity.user_id))
        connection.commit()

Users can update existing Sport Activity records. Below code is used for update operation.

.. code-block:: python

    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()  # prevented sql injection
        statement = """SELECT ID FROM USERS WHERE (USERS.USERNAME = %s) AND (USERS.EMAIL = %s)"""
        cursor.execute(statement, (username, email))
        activity_user_id = cursor.fetchone()
        activityid = request.form['activity-id']

        activityName = request.form['InputActivityName']
        if not activityName:
            statement = """SELECT NAME FROM SPORTACTIVITIES WHERE SPORTACTIVITIES.ID = %s"""
            cursor.execute(statement, activityid)
            activityName = cursor.fetchone()

        sportName = request.form['InputSportName']
        if not sportName:
            statement = """SELECT SPORTNAME FROM SPORTACTIVITIES WHERE SPORTACTIVITIES.ID = %s"""
            cursor.execute(statement, activityid)
            sportName = cursor.fetchone()

        activityDate = request.form['InputActivityDate']
        if not activityDate:
            statement = """SELECT ACTIVITYDATE FROM SPORTACTIVITIES WHERE SPORTACTIVITIES.ID = %s"""
            cursor.execute(statement, activityid)
            activityDate = cursor.fetchone()

        activityTime = request.form['InputActivityTime']
        if not activityTime:
            statement = """SELECT ACTIVITYTIME FROM SPORTACTIVITIES WHERE SPORTACTIVITIES.ID = %s"""
            cursor.execute(statement, activityid)
            activityTime = cursor.fetchone()

        activityLoc = request.form['InputActivityLocation']
        if not activityLoc:
            statement = """SELECT LOCATION FROM SPORTACTIVITIES WHERE SPORTACTIVITIES.ID = %s"""
            cursor.execute(statement, activityid)
            activityLoc = cursor.fetchone()

        activityDesc = request.form['ActivityDescription']
        if not activityDesc:
            statement = """SELECT DESCRIPTION FROM SPORTACTIVITIES WHERE SPORTACTIVITIES.ID = %s"""
            cursor.execute(statement, activityid)
            activityDesc = cursor.fetchone()


The below code updates the existing record via using this query.

.. code-block:: python

    statement = """UPDATE SPORTACTIVITIES SET NAME = %s, SPORTNAME = %s, ACTIVITYDATE = %s, ACTIVITYTIME = %s, LOCATION = %s, DESCRIPTION = %s, USERID = %s WHERE SPORTACTIVITIES.ID = %s"""
    cursor.execute(statement,
        (activityName, sportName, activityDate, activityTime, activityLoc, activityDesc, activity_user_id, activityid))
    connection.commit()

.. raw:: latex

    \newpage