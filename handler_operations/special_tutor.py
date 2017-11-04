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

from classes.special_tutors_class import special_tutor

from server import load_user

def special_tutor_page():
    if request.method == "POST":
        username = current_user.get_username()
        email = current_user.get_email()
        name = current_user.get_name()
        surname = current_user.get_surname()
        tutorsubject = request.form['SpecialTutorSubject']
        tutorname = request.form['SpecialTutorName']
        if not tutorname:
            seq = {name, surname}
            tutorname = " ".join(seq)
        tutormail = request.form['SpecialTutorMail']
        if not tutormail:
            tutormail = email
        tutorphone = request.form['SpecialTutorPhone']

        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            statement = """SELECT ID FROM USERS WHERE (USERS.USERNAME = %s) AND (USERS.EMAIL = %s)"""
            cursor.execute(statement, (username, email))
            tutorid = cursor.fetchone()

            tutor = special_tutor(tutorsubject, tutorname, tutormail, tutorphone, tutorid)
            query = """INSERT INTO SPECIALTUTORS(SUBJECT, FULLNAME, EMAIL, PHONENUMBER, USERID) VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(query, (tutor.subject, tutor.fullname, tutor.email, tutor.phonenumber, tutor.user_id))
            connection.commit()
        return redirect(url_for('siteSpecialStudent'))
    else:
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """SELECT SUBJECT, FULLNAME, EMAIL, PHONENUMBER FROM SPECIALTUTORS"""
            cursor.execute(query)
            specialtutors = cursor.fetchall()
        return render_template('special_tutor.html', specialtutors=specialtutors)