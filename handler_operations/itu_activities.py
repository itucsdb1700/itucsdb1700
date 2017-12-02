from flask import render_template
from flask import current_app
from flask import request
from flask_login import current_user
from flask import session

from flask import redirect
from flask.helpers import url_for

from classes.itu_activity_class import ItuActivity

import psycopg2 as dbapi2


def itu_activity_page():
    if request.method == 'POST':
        if 'userSearchButton' in request.form:  # if the search button is submitted
            session['search_username'] = request.form['usernameSearch']
            return redirect(url_for('site.SearchUserPage'))

        formtype = request.form['form-name']
        username = current_user.get_username()
        email = current_user.get_email()

        if formtype == "Activity":
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

                ituActivity = ItuActivity(activityName, participantName, activityDate, activityTime, activityLoc,
                                          activityDesc, UserId)

                cursor = connection.cursor()
                query = """INSERT INTO ITUACTIVITIES (NAME, SPECIALPARTICIPANT, ACTIVITYDATE, ACTIVITYTIME, LOCATION, DESCRIPTION, USERID) 
                                                                        VALUES(%s,%s,%s,%s,%s,%s,%s)"""
                cursor.execute(query, (ituActivity.activityName, ituActivity.participantName,
                                       ituActivity.activityDate, ituActivity.activityTime,
                                       ituActivity.activityLoc, ituActivity.activityDesc, ituActivity.user_id))
                connection.commit()

            return redirect(url_for('site.ItuActivityPage'))

        elif formtype == "ActivityUpdate":
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


                statement = """UPDATE ITUACTIVITIES SET NAME = %s, SPECIALPARTICIPANT = %s, ACTIVITYDATE = %s, ACTIVITYTIME = %s, LOCATION = %s, DESCRIPTION = %s, USERID = %s WHERE ITUACTIVITIES.ID = %s"""
                cursor.execute(statement,
                               (activityName, participantName, activityDate, activityTime, activityLoc, activityDesc, activity_user_id, activityid))
                connection.commit()
                return redirect(url_for('site.SelectedItuActivity', activityId=activityid))


    else:
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """SELECT ITUACTIVITIES.NAME, SPECIALPARTICIPANT, ACTIVITYDATE, ACTIVITYTIME, LOCATION, DESCRIPTION, 
            USERS.NAME, USERS.SURNAME, USERS.EMAIL, FACULTIES.FACULTYNAME, FACULTIES.FACULTYCODE, USERS.USERNAME, ITUACTIVITIES.ID  
            FROM ITUACTIVITIES, USERS, FACULTIES 
            WHERE (ITUACTIVITIES.USERID = USERS.ID) AND (USERS.FACULTYID = FACULTIES.ID)"""
            cursor.execute(query)
            ituActivities = cursor.fetchall()

        return render_template('itu_activities.html', ituActivities=ituActivities)
