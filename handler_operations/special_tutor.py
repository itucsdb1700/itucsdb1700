from flask import render_template, Blueprint, current_app, session, redirect, request
from flask.helpers import url_for
from flask_login import current_user, login_user, logout_user, login_required, LoginManager

import psycopg2 as dbapi2

from server import load_user
from user import User, get_user
from passlib.apps import custom_app_context as pwd_context
from datetime import datetime
import os.path

from classes.special_tutors_class import special_tutor

def special_tutor_page():
    if request.method == "POST":
        if 'userSearchButton' in request.form: #if the search button is submitted
            session['search_username'] = request.form['usernameSearch']
            return redirect(url_for('site.SearchUserPage'))

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
        return redirect(url_for('site.SpecialTutor'))
    else:
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """SELECT SUBJECT, FULLNAME, SPECIALTUTORS.EMAIL, PHONENUMBER, USERS.USERNAME FROM SPECIALTUTORS, USERS WHERE (SPECIALTUTORS.USERID = USERS.ID)"""
            cursor.execute(query)
            specialtutors = cursor.fetchall()
        return render_template('special_tutor.html', specialtutors=specialtutors)