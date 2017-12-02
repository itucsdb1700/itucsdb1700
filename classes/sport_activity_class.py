from flask import current_app
import psycopg2 as dbapi2

class SportActivity:
    def __init__(self, activityName, sportName, activityDate, activityTime, activityLoc, activityDesc, user_id):
        self.activityName = activityName
        self.sportName = sportName
        self.activityDate = activityDate
        self.activityTime = activityTime
        self.activityLoc = activityLoc
        self.activityDesc = activityDesc
        self.user_id = user_id


    def get_activityName(self):
        return self.activityName
    def get_sportName(self):
        return self.sportName
    def get_activityDate(self):
        return self.activityDate
    def get_activityTime(self):
        return self.activityTime
    def get_activityLoc(self):
        return self.activityLoc
    def get_activityDesc(self):
        return self.activityDesc
    def get_user_id(self):
        return self.user_id
    def get_id(self):
        return self.id


    def get_activity_byId(activityId):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            statement = """SELECT * FROM SPORTACTIVITIES WHERE SPORTACTIVITIES.ID = %s"""
            cursor.execute(statement, [activityId])
            db_activity = cursor.fetchall()
            activity = SportActivity(db_activity[0][1], db_activity[0][2], db_activity[0][3], db_activity[0][4],
                                   db_activity[0][5], db_activity[0][6], db_activity[0][7])
            activity.id = db_activity[0][0]
            return activity


    def delete_activity_byId(activityId):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            statement = """DELETE FROM SPORTACTIVITIES WHERE SPORTACTIVITIES.ID = %s"""
            cursor.execute(statement, [activityId])
