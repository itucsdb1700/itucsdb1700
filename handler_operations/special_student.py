from flask import render_template, Blueprint
from flask import current_app
from datetime import datetime

from flask import redirect
from flask.helpers import url_for

from flask_login import login_required
from flask_login import current_user, login_user, logout_user
from user import User
from user import get_user
from flask_login import LoginManager
from flask import request


from passlib.apps import custom_app_context as pwd_context

import psycopg2 as dbapi2
import os.path

from classes.special_students_class import special_student

from server import load_user

def special_student_page():
    if request.method == "POST":
        username = current_user.get_username()
        email = current_user.get_email()
        name = current_user.get_name()
        surname = current_user.get_surname()
        studentsubject = request.form['SpecialStudentSubject']
        studentname = request.form['SpecialStudentName']
        if not studentname:
            seq = {name, surname}
            studentname = " ".join(seq)
        studentmail = request.form['SpecialStudentMail']
        if not studentmail:
            studentmail = email
        studentphone = request.form['SpecialStudentPhone']

        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            statement = """SELECT ID FROM USERS WHERE (USERS.USERNAME = %s) AND (USERS.EMAIL = %s)"""
            cursor.execute(statement, (username, email))
            studentid = cursor.fetchone()

            student = special_student(studentsubject, studentname, studentmail, studentphone, studentid)
            query = """INSERT INTO SPECIALSTUDENTS(SUBJECT, FULLNAME, EMAIL, PHONENUMBER, USERID) VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(query, (student.subject, student.fullname, student.email, student.phonenumber, student.user_id))
            connection.commit()
        return redirect(url_for('site.SpecialStudent'))
    else:
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """SELECT SUBJECT, FULLNAME, EMAIL, PHONENUMBER FROM SPECIALSTUDENTS"""
            cursor.execute(query)
            specialstudents = cursor.fetchall()
        return render_template('special_student.html', specialstudents=specialstudents)