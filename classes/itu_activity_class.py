from flask import current_app
import psycopg2 as dbapi2

class ItuActivity:
    def __init__(self, activityName, participantName, activityDate, activityTime, activityLoc, activityDesc ,user_id):
        self.activityName = activityName
        self.participantName = participantName
        self.activityDate = activityDate
        self.activityTime = activityTime
        self.activityLoc = activityLoc
        self.activityDesc = activityDesc
        self.user_id = user_id


    def get_activityName(self):
        return self.activityName
    def get_participantName(self):
        return self.participantName
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
            statement = """SELECT * FROM ITUACTIVITIES WHERE ITUACTIVITIES.ID = %s"""
            cursor.execute(statement, [activityId])
            db_activity = cursor.fetchall()
            activity = ItuActivity(db_activity[0][1], db_activity[0][2], db_activity[0][5], db_activity[0][3],
                                   db_activity[0][4], db_activity[0][6], db_activity[0][7])
            activity.id = db_activity[0][0]
            return activity


    def delete_activity_byId(activityId):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            statement = """DELETE FROM ITUACTIVITIES WHERE ITUACTIVITIES.ID = %s"""
            cursor.execute(statement, [activityId])
