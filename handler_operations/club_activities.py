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

        formtype = request.form['form-name']
        username = current_user.get_username()
        email = current_user.get_email()

        if formtype == "Activity":
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

                clubActivity = ClubActivity(activityName, clubName, activityDate, activityTime, activityLoc,
                                            activityDesc, UserId)

                cursor = connection.cursor()
                query = """INSERT INTO CLUBACTIVITIES (NAME, CLUBNAME, ACTIVITYDATE, ACTIVITYTIME, LOCATION, DESCRIPTION, USERID) 
                                                            VALUES(%s,%s,%s,%s,%s,%s,%s)"""
                cursor.execute(query, (clubActivity.activityName, clubActivity.clubName,
                                       clubActivity.activityDate, clubActivity.activityTime,
                                       clubActivity.activityLoc, clubActivity.activityDesc, clubActivity.user_id))
                connection.commit()

            return redirect(url_for('site.ClubActivityPage'))

        elif formtype == "ActivityUpdate":
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


                statement = """UPDATE CLUBACTIVITIES SET NAME = %s, CLUBNAME = %s, ACTIVITYDATE = %s, ACTIVITYTIME = %s, LOCATION = %s, DESCRIPTION = %s, USERID = %s WHERE CLUBACTIVITIES.ID = %s"""
                cursor.execute(statement,
                               (activityName, clubName, activityDate, activityTime, activityLoc, activityDesc, activity_user_id, activityid))
                connection.commit()
                return redirect(url_for('site.SelectedClubActivity', activityId=activityid))



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
