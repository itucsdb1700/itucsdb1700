from flask import current_app
from flask_login import UserMixin
import psycopg2 as dbapi2

class special_tutor:
    def __init__(self, subject, fullname, email, phonenumber, user_id):
        self.subject = subject
        self.fullname = fullname
        self.email = email
        self.phonenumber = phonenumber
        self.user_id = user_id

    def get_subject(self):
        return self.subject
    def get_name(self):
        return self.fullname
    def get_mail(self):
        return self.email
    def get_phone(self):
        return self.phonenumber
    def get_user_id(self):
        return self.user_id
    def get_id(self):
        return self.id

    def get_tutor_byId(tutorId):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            statement = """SELECT * FROM SPECIALTUTORS WHERE SPECIALTUTORS.ID = %s"""
            cursor.execute(statement, [tutorId])
            db_tutor = cursor.fetchall()
            tutor = special_tutor(db_tutor[0][1], db_tutor[0][2], db_tutor[0][3], db_tutor[0][4], db_tutor[0][5])
            tutor.id = db_tutor[0][0]
            return tutor

    def delete_tutor_byId(tutorId):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            statement = """DELETE FROM SPECIALTUTORS WHERE SPECIALTUTORS.ID = %s"""
            cursor.execute(statement, [tutorId])