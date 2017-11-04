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

def shared_LessonNotes_Announcement_Page():
    if request.method == "POST":
        formtype = request.form['form-name']

        username = current_user.get_username()
        email = current_user.get_email()
        if formtype == "SharedLessonNotesAnnouncement":
            NameOfLessonNote = request.form['InputNameOfSharedLessonNote']
            TeacherName = request.form['InputTeacherNameofSharedLessonNote']
            LessonName = request.form['InputLessonNameOfShareLessonNote']
            LessonCode = request.form['InputLessonCodeOfShareLessonNote']

            with dbapi2.connect(current_app.config['dsn']) as connection:
                cursor = connection.cursor()

                statement = """SELECT ID FROM USERS
                                  WHERE(USERS.USERNAME = %s)
                                  AND(USERS.EMAIL = %s)"""
                cursor.execute(statement, (username, email))
                currentuser_id = cursor.fetchone()
                query = """INSERT INTO SHAREDLESSONNOTES(NAMEOFNOTES, LESSONNAME, LESSONCODE,TEACHERNAME,USERID)
                                                                        VALUES (%s,%s,%s,%s,%s)"""

                cursor.execute(query, (NameOfLessonNote,LessonName,LessonCode,TeacherName,currentuser_id))

                connection.commit()
        return render_template("sharedbooks_announcement.html")
    else:
        return render_template("sharedbooks_announcement.html")