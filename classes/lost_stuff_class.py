from flask import current_app
from flask_login import UserMixin
import psycopg2 as dbapi2

class lost_stuff:
    def __init__(self, lostdesc, lostlocation, lostdate, lostownername, lostmail, lostphone, lostuser_id):
        self.description = lostdesc
        self.location = lostlocation
        self.date = lostdate
        self.ownername = lostownername
        self.mail = lostmail
        self.phone = lostphone
        self.user_id = lostuser_id
    def get_desc(self):
        return self.description
    def get_location(self):
        return self.location
    def get_date(self):
        return self.date
    def get_name(self):
        return self.ownername
    def get_mail(self):
        return self.mail
    def get_phone(self):
        return self.phone
    def get_user_id(self):
        return self.user_id
    def get_id(self):
        return self.id

    def get_lost_byId(lostId):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            statement = """SELECT * FROM LOSTSTUFF WHERE LOSTSTUFF.ID = %s"""
            cursor.execute(statement, [lostId])
            db_lost = cursor.fetchall()
            lost = lost_stuff(db_lost[0][1], db_lost[0][2], db_lost[0][3], db_lost[0][4], db_lost[0][5], db_lost[0][6], db_lost[0][7])
            lost.id = db_lost[0][0]
            return lost

    def delete_lost_byId(lostId):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            statement = """DELETE FROM LOSTSTUFF WHERE LOSTSTUFF.ID = %s"""
            cursor.execute(statement, [lostId])