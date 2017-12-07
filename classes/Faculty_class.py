from flask import current_app
from flask_login import UserMixin
import psycopg2 as dbapi2

class Faculty:
    def __init__(self, facultyName, facultyCode):
        self.facultyName = facultyName
        self.facultyCode = facultyCode

    def get_name(self):
        return self.facultyName
    def get_code(self):
        return self.facultyCode
    def get_id(self):
        return self.id

    def get_faculty_byId(facultyId):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            statement = """SELECT * FROM FACULTIES WHERE FACULTIES.ID = %s"""
            cursor.execute(statement, [facultyId])
            db_found = cursor.fetchall()
            faculty = Faculty(db_found[0][1], db_found[0][2])
            faculty.id = db_found[0][0]
            return faculty

    def delete_faculty_byId(id):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            statement = """DELETE FROM FACULTIES WHERE ID = %s"""
            cursor.execute(statement, [id])