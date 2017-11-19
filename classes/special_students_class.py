from flask import current_app
from flask_login import UserMixin
import psycopg2 as dbapi2

class special_student:
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

    def get_student_byId(studentId):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            statement = """SELECT * FROM SPECIALSTUDENTS WHERE SPECIALSTUDENTS.ID = %s"""
            cursor.execute(statement, [studentId])
            db_student = cursor.fetchall()
            student = special_student(db_student[0][1], db_student[0][2], db_student[0][3], db_student[0][4], db_student[0][5])
            student.id = db_student[0][0]
            return student

    def delete_student_byId(studentId):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            statement = """DELETE FROM SPECIALSTUDENTS WHERE SPECIALSTUDENTS.ID = %s"""
            cursor.execute(statement, [studentId])