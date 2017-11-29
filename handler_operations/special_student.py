from flask import render_template, Blueprint, current_app, session, redirect, request
from flask.helpers import url_for
from flask_login import current_user, login_user, logout_user, login_required, LoginManager

import psycopg2 as dbapi2

from server import load_user
from user import User, get_user
from passlib.apps import custom_app_context as pwd_context
from datetime import datetime
import os.path

from classes.special_students_class import special_student

def special_student_page():
    if request.method == "POST":
        if 'userSearchButton' in request.form:  # if the search button is submitted
            session['search_username'] = request.form['usernameSearch']
            return redirect(url_for('site.SearchUserPage'))
        formtype = request.form['form-name']

        username = current_user.get_username()
        email = current_user.get_email()
        name = current_user.get_name()
        surname = current_user.get_surname()
        if formtype == "SpecialStudent":
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
        elif formtype == "SpecialStudentUpdate":
            with dbapi2.connect(current_app.config['dsn']) as connection:
                cursor = connection.cursor()  # prevented sql injection
                statement = """SELECT ID FROM USERS WHERE (USERS.USERNAME = %s) AND (USERS.EMAIL = %s)"""
                cursor.execute(statement, (username, email))
                studentuser_id = cursor.fetchone()
                studentid = request.form['student-id']

                studentsubject = request.form['SpecialStudentSubject']
                if not studentsubject:
                    statement = """SELECT SUBJECT FROM SPECIALSTUDENTS WHERE SPECIALSTUDENTS.ID = %s"""
                    cursor.execute(statement, studentid)
                    studentsubject = cursor.fetchone()

                studentname = request.form['SpecialStudentName']
                if not studentname:
                    statement = """SELECT FULLNAME FROM SPECIALSTUDENTS WHERE SPECIALSTUDENTS.ID = %s"""
                    cursor.execute(statement, studentid)
                    studentname = cursor.fetchone()

                studentmail = request.form['SpecialStudentMail']
                if not studentmail:
                    statement = """SELECT EMAIL FROM SPECIALSTUDENTS WHERE SPECIALSTUDENTS.ID = %s"""
                    cursor.execute(statement, studentid)
                    studentmail = cursor.fetchone()

                studentphone = request.form['SpecialStudentPhone']
                if not studentphone:
                    statement = """SELECT PHONENUMBER FROM SPECIALSTUDENTS WHERE SPECIALSTUDENTS.ID = %s"""
                    cursor.execute(statement, studentid)
                    studentphone = cursor.fetchone()

                statement = """UPDATE SPECIALSTUDENTS SET SUBJECT = %s, FULLNAME = %s, EMAIL = %s, PHONENUMBER = %s, USERID = %s WHERE SPECIALSTUDENTS.ID = %s"""
                cursor.execute(statement, (studentsubject, studentname, studentmail, studentphone, studentuser_id, studentid))
                connection.commit()
                return redirect(url_for('site.selected_special_student', studentId=studentid))

    else:
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """SELECT SUBJECT, FULLNAME, SPECIALSTUDENTS.EMAIL, PHONENUMBER, USERS.USERNAME, SPECIALSTUDENTS.ID FROM SPECIALSTUDENTS, USERS WHERE (SPECIALSTUDENTS.USERID = USERS.ID)"""
            cursor.execute(query)
            specialstudents = cursor.fetchall()
        return render_template('special_student.html', specialstudents=specialstudents)