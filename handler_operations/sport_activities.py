from flask import render_template
from flask import current_app
from flask import request
from flask_login import current_user
from flask import session

from flask import redirect
from flask.helpers import url_for

from classes.sport_activity_class import SportActivity

import psycopg2 as dbapi2


def sport_activity_page():
    if request.method == 'POST':
        if 'userSearchButton' in request.form:  # if the search button is submitted
            session['search_username'] = request.form['usernameSearch']
            return redirect(url_for('site.SearchUserPage'))

        formtype = request.form['form-name']
        username = current_user.get_username()
        email = current_user.get_email()

        if formtype == "Activity":
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

                sportActivity = SportActivity(activityName, sportName, activityDate, activityTime, activityLoc,
                                              activityDesc, UserId)

                cursor = connection.cursor()
                query = """INSERT INTO SPORTACTIVITIES (NAME, SPORTNAME, ACTIVITYDATE, ACTIVITYTIME, LOCATION, DESCRIPTION, USERID) 
                            VALUES(%s,%s,%s,%s,%s,%s,%s)"""
                cursor.execute(query, (sportActivity.activityName, sportActivity.sportName,
                                       sportActivity.activityDate, sportActivity.activityTime,
                                       sportActivity.activityLoc, sportActivity.activityDesc, sportActivity.user_id))
                connection.commit()

            return redirect(url_for('site.SportActivityPage'))

        elif formtype == "ActivityUpdate":
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


                statement = """UPDATE SPORTACTIVITIES SET NAME = %s, SPORTNAME = %s, ACTIVITYDATE = %s, ACTIVITYTIME = %s, LOCATION = %s, DESCRIPTION = %s, USERID = %s WHERE SPORTACTIVITIES.ID = %s"""
                cursor.execute(statement,
                               (activityName, sportName, activityDate, activityTime, activityLoc, activityDesc, activity_user_id, activityid))
                connection.commit()
                return redirect(url_for('site.SelectedSportActivity', activityId=activityid))



    else:
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """SELECT SPORTACTIVITIES.NAME, SPORTNAME, ACTIVITYDATE, ACTIVITYTIME, LOCATION, DESCRIPTION, 
            USERS.NAME, USERS.SURNAME, USERS.EMAIL, FACULTIES.FACULTYNAME, FACULTIES.FACULTYCODE, USERS.USERNAME, SPORTACTIVITIES.ID 
            FROM SPORTACTIVITIES, USERS, FACULTIES 
            WHERE (SPORTACTIVITIES.USERID = USERS.ID) AND (USERS.FACULTYID = FACULTIES.ID)"""
            cursor.execute(query)
            sportActivities = cursor.fetchall()

        return render_template('sport_activities.html', sportActivities=sportActivities)
