from flask import render_template
from flask import current_app
from flask import request
from flask_login import current_user
from flask import session

from flask import redirect
from flask.helpers import url_for

from classes.club_activity_class import ClubActivity

import psycopg2 as dbapi2


def club_activity_page():
    if request.method == 'POST':
        if 'userSearchButton' in request.form:  # if the search button is submitted
            session['search_username'] = request.form['usernameSearch']
            return redirect(url_for('site.SearchUserPage'))

        # current user information is taken
        username = current_user.get_username()
        email = current_user.get_email()
        # name = current_user.get_name()
        # surname = current_user.get_surname()

        activityName = request.form['InputActivityName']
        clubName = request.form['InputClubName']
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

            clubActivity = ClubActivity(activityName, clubName, activityDate, activityTime, activityLoc, activityDesc, UserId)

            cursor = connection.cursor()
            query = """INSERT INTO CLUBACTIVITIES (NAME, CLUBNAME, ACTIVITYDATE, ACTIVITYTIME, LOCATION, DESCRIPTION, USERID) 
                                                VALUES(%s,%s,%s,%s,%s,%s,%s)"""
            cursor.execute(query, (clubActivity.activityName, clubActivity.clubName,
                                   clubActivity.activityDate, clubActivity.activityTime,
                                   clubActivity.activityLoc, clubActivity.activityDesc, clubActivity.user_id))
            connection.commit()

        return redirect(url_for('site.ClubActivityPage'))

    else:
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """SELECT CLUBACTIVITIES.NAME, CLUBNAME, ACTIVITYDATE, ACTIVITYTIME, LOCATION, DESCRIPTION, 
            USERS.NAME, USERS.SURNAME, USERS.EMAIL, FACULTIES.FACULTYNAME, FACULTIES.FACULTYCODE, USERS.USERNAME, CLUBACTIVITIES.ID
            FROM CLUBACTIVITIES, USERS, FACULTIES 
            WHERE (CLUBACTIVITIES.USERID = USERS.ID) AND (USERS.FACULTYID = FACULTIES.ID)"""
            cursor.execute(query)
            clubActivities = cursor.fetchall()

        return render_template('club_activities.html', clubActivities=clubActivities)
