from flask import render_template
from flask import current_app
from flask import request

from classes.club_activity_class import ClubActivity

import psycopg2 as dbapi2


def club_activity_page():
    if request.method == 'POST':
        activityName = request.form['InputActivityName']
        clubName = request.form['InputClubName']
        activityDate = request.form['InputActivityDate']
        activityTime = request.form['InputActivityTime']
        activityLoc = request.form['InputActivityLocation']
        activityDesc = request.form['ActivityDescription']

        clubActivity = ClubActivity(activityName,clubName,activityDate,activityTime,activityLoc,activityDesc)

        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()

            query = """INSERT INTO GAMEFRIEND (NAME, TYPE, GAMEDATE, LOCATION, PLAYERNUMBER, DESCRIPTION) 
                                                VALUES('%s', '%s', '%s', '%s', '%d', '%s')""" % (
                clubActivity.activityName, clubActivity.clubName, clubActivity.activityDate,
                clubActivity.activityTime, clubActivity.activityLoc, clubActivity.activityDesc)

            cursor.execute(query)
            connection.commit()

        return render_template('club_activities.html')

    else:
        return render_template('club_activities.html')
