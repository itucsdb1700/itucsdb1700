from flask import render_template
from flask import current_app
from flask import request
from flask_login import current_user

from flask import redirect
from flask.helpers import url_for

from classes.itu_activity_class import ItuActivity

import psycopg2 as dbapi2


def itu_activity_page():
    if request.method == 'POST':
        # current user information is taken
        username = current_user.get_username()
        email = current_user.get_email()
        # name = current_user.get_name()
        # surname = current_user.get_surname()

        activityName = request.form['InputActivityName']
        participantName = request.form['InputParticipantName']
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

            ituActivity = ItuActivity(activityName, participantName, activityDate, activityTime, activityLoc, activityDesc, UserId)

            cursor = connection.cursor()
            query = """INSERT INTO ITUACTIVITIES (NAME, SPECIALPARTICIPANT, ACTIVITYDATE, ACTIVITYTIME, LOCATION, DESCRIPTION, USERID) 
                                                            VALUES(%s,%s,%s,%s,%s,%s,%s)"""
            cursor.execute(query, (ituActivity.activityName, ituActivity.participantName,
                                   ituActivity.activityDate, ituActivity.activityTime,
                                   ituActivity.activityLoc, ituActivity.activityDesc, ituActivity.user_id))
            connection.commit()

        return redirect(url_for('site.ItuActivityPage'))

    else:
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """SELECT ITUACTIVITIES.NAME, SPECIALPARTICIPANT, ACTIVITYDATE, ACTIVITYTIME, LOCATION, DESCRIPTION, 
            USERS.NAME, USERS.SURNAME, USERS.EMAIL, FACULTIES.FACULTYNAME, FACULTIES.FACULTYCODE 
            FROM ITUACTIVITIES, USERS, FACULTIES 
            WHERE (ITUACTIVITIES.USERID = USERS.ID) AND (USERS.FACULTYID = FACULTIES.ID)"""
            cursor.execute(query)
            ituActivities = cursor.fetchall()

        return render_template('itu_activities.html', ituActivities=ituActivities)
