from flask import render_template
from flask import current_app
from flask import request
from flask_login import current_user

from flask import redirect
from flask.helpers import url_for

from classes.sport_activity_class import SportActivity

import psycopg2 as dbapi2


def sport_activity_page():
    if request.method == 'POST':
        # current user information is taken
        username = current_user.get_username()
        email = current_user.get_email()
        # name = current_user.get_name()
        # surname = current_user.get_surname()

        activityName = request.form['InputActivityName']
        sportName = request.form['InputSportName']
        activityDate = request.form['InputActivityDate']
        activityTime = request.form['InputActivityTime']
        activityLoc = request.form['InputActivityLocation']
        activityDesc = request.form['ActivityDescription']



        with dbapi2.connect(current_app.config['dsn']) as connection:
            # to take the current user's name and email
            cursor1 = connection.cursor()
            statement = """SELECT ID FROM USERS WHERE (USERS.USERNAME = %s) AND (USERS.EMAIL = %s)"""
            cursor1.execute(statement, (username, email))
            UserId = cursor1.fetchone()
            UserId = UserId[0]

            sportActivity = SportActivity(activityName, sportName, activityDate, activityTime, activityLoc, activityDesc, UserId)

            cursor = connection.cursor()
            query = """INSERT INTO SPORTACTIVITIES (NAME, SPORTNAME, ACTIVITYDATE, ACTIVITYTIME, LOCATION, DESCRIPTION, USERID) 
                VALUES(%s,%s,%s,%s,%s,%s,%s)"""
            cursor.execute(query, (sportActivity.activityName, sportActivity.sportName,
                                   sportActivity.activityDate, sportActivity.activityTime,
                                   sportActivity.activityLoc, sportActivity.activityDesc, sportActivity.user_id))
            connection.commit()

        return redirect(url_for('site.SportActivityPage'))

    else:
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """SELECT SPORTACTIVITIES.NAME, SPORTNAME, ACTIVITYDATE, ACTIVITYTIME, LOCATION, DESCRIPTION, 
            USERS.NAME, USERS.SURNAME, USERS.EMAIL, FACULTIES.FACULTYNAME, FACULTIES.FACULTYCODE 
            FROM SPORTACTIVITIES, USERS, FACULTIES 
            WHERE (SPORTACTIVITIES.USERID = USERS.ID) AND (USERS.FACULTYID = FACULTIES.ID)"""
            cursor.execute(query)
            sportActivities = cursor.fetchall()

        return render_template('sport_activities.html', sportActivities=sportActivities)
