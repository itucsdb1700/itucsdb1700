from flask import render_template
from flask import current_app
from flask import request

from classes.sport_activity_class import SportActivity

import psycopg2 as dbapi2


def sport_activity_page():
    if request.method == 'POST':
        activityName = request.form['InputActivityName']
        sportName = request.form['InputSportName']
        activityDate = request.form['InputActivityDate']
        activityTime = request.form['InputActivityTime']
        activityLoc = request.form['InputActivityLocation']
        activityDesc = request.form['ActivityDescription']

        sportActivity = SportActivity(activityName,sportName,activityDate,activityTime,activityLoc,activityDesc)

        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()

            query = """INSERT INTO GAMEFRIEND (NAME, TYPE, GAMEDATE, LOCATION, PLAYERNUMBER, DESCRIPTION) 
                                                VALUES('%s', '%s', '%s', '%s', '%d', '%s')""" % (
                sportActivity.activityName, sportActivity.sportName, sportActivity.activityDate,
                sportActivity.activityTime, sportActivity.activityLoc, sportActivity.activityDesc)

            cursor.execute(query)
            connection.commit()

        return render_template('sport_activities.html')

    else:
        return render_template('sport_activities.html')
