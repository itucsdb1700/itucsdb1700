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
        formtype = request.form['form-name']

        username = current_user.get_username()
        email = current_user.get_email()
        name = current_user.get_name()
        surname = current_user.get_surname()
        if formtype == "SpecialTutor":
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
        elif formtype == "SpecialTutorUpdate":
            with dbapi2.connect(current_app.config['dsn']) as connection:
                cursor = connection.cursor()  # prevented sql injection
                statement = """SELECT ID FROM USERS WHERE (USERS.USERNAME = %s) AND (USERS.EMAIL = %s)"""
                cursor.execute(statement, (username, email))
                tutoruser_id = cursor.fetchone()
                tutorid = request.form['tutor-id']

                tutorsubject = request.form['SpecialTutorSubject']
                if not tutorsubject:
                    statement = """SELECT SUBJECT FROM SPECIALTUTORS WHERE SPECIALTUTORS.ID = %s"""
                    cursor.execute(statement, tutorid)
                    tutorsubject = cursor.fetchone()

                tutorname = request.form['SpecialTutorName']
                if not tutorname:
                    statement = """SELECT FULLNAME FROM SPECIALTUTORS WHERE SPECIALTUTORS.ID = %s"""
                    cursor.execute(statement, tutorid)
                    tutorname = cursor.fetchone()

                tutormail = request.form['SpecialTutorMail']
                if not tutormail:
                    statement = """SELECT EMAIL FROM SPECIALTUTORS WHERE SPECIALTUTORS.ID = %s"""
                    cursor.execute(statement, tutorid)
                    tutormail = cursor.fetchone()

                tutorphone = request.form['SpecialTutorPhone']
                if not tutorphone:
                    statement = """SELECT PHONENUMBER FROM SPECIALTUTORS WHERE SPECIALTUTORS.ID = %s"""
                    cursor.execute(statement, tutorid)
                    tutorphone = cursor.fetchone()

                statement = """UPDATE SPECIALTUTORS SET SUBJECT = %s, FULLNAME = %s, EMAIL = %s, PHONENUMBER = %s, USERID = %s WHERE SPECIALTUTORS.ID = %s"""
                cursor.execute(statement,
                               (tutorsubject, tutorname, tutormail, tutorphone, tutoruser_id, tutorid))
                connection.commit()
                return redirect(url_for('site.selected_special_tutor', tutorId=tutorid))
    else:
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """SELECT SUBJECT, FULLNAME, SPECIALTUTORS.EMAIL, PHONENUMBER, USERS.USERNAME, SPECIALTUTORS.ID FROM SPECIALTUTORS, USERS WHERE (SPECIALTUTORS.USERID = USERS.ID)"""
            cursor.execute(query)
            specialtutors = cursor.fetchall()
        return render_template('special_tutor.html', specialtutors=specialtutors)