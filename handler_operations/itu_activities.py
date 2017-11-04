from flask import render_template
from flask import current_app
from flask import request

from classes.itu_activity_class import ItuActivity

import psycopg2 as dbapi2


def itu_activity_page():
    if request.method == 'POST':
        activityName = request.form['InputActivityName']
        participantName = request.form['InputParticipantName']
        activityDate = request.form['InputActivityDate']
        activityTime = request.form['InputActivityTime']
        activityLoc = request.form['InputActivityLocation']
        activityDesc = request.form['ActivityDescription']

        ituActivity = ItuActivity(activityName,participantName,activityDate,activityTime,activityLoc,activityDesc)

        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()

            query = """INSERT INTO GAMEFRIEND (NAME, TYPE, GAMEDATE, LOCATION, PLAYERNUMBER, DESCRIPTION) 
                                                VALUES('%s', '%s', '%s', '%s', '%d', '%s')""" % (
                ituActivity.activityName, ituActivity.participantName, ituActivity.activityDate,
                ituActivity.activityTime, ituActivity.activityLoc, ituActivity.activityDesc)

            cursor.execute(query)
            connection.commit()

        return render_template('itu_activities.html')

    else:
        return render_template('itu_activities.html')
