from flask import current_app
from flask_login import UserMixin
import psycopg2 as dbapi2

class found_stuff:
    def __init__(self, founddesc, foundlocation, founddate, foundname, foundmail, foundphone, founduser_id):
        self.description = founddesc
        self.location = foundlocation
        self.date = founddate
        self.name = foundname
        self.mail = foundmail
        self.phone = foundphone
        self.user_id = founduser_id

    def get_desc(self):
        return self.description
    def get_location(self):
        return self.location
    def get_date(self):
        return self.date
    def get_name(self):
        return self.name
    def get_mail(self):
        return self.mail
    def get_phone(self):
        return self.phone
    def get_user_id(self):
        return self.user_id
    def get_id(self):
        return self.id

    def get_found_byId(foundId):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            statement = """SELECT * FROM FOUNDSTUFF WHERE FOUNDSTUFF.ID = %s"""
            cursor.execute(statement, [foundId])
            db_found = cursor.fetchall()
            found = found_stuff(db_found[0][1], db_found[0][2], db_found[0][3], db_found[0][4], db_found[0][5], db_found[0][6], db_found[0][7])
            found.id = db_found[0][0]
            return found

    def delete_found_byId(foundId):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            statement = """DELETE FROM FOUNDSTUFF WHERE FOUNDSTUFF.ID = %s"""
            cursor.execute(statement, [foundId])