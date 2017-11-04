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


def shared_Books_Announcement_Page():
    if request.method == "POST":
        formtype = request.form['form-name']

        username = current_user.get_username()
        email = current_user.get_email()
        if formtype == "SharedBooksAnnouncement":
            NameOfBook = request.form['InputNameOfSharedBook']
            LessonName = request.form['InputLessonNameOfShareBook']
            LessonCode = request.form['InputLessonCodeOfShareBook']
            TypeOfShare = request.form['InputTypeOfSharedBooks']
            if(request.form['InputPriceOfShareBook']):
                Price = request.form['InputPriceOfShareBook']
            else:
                Price = None

            with dbapi2.connect(current_app.config['dsn']) as connection:
                cursor = connection.cursor()

                statement = """SELECT ID FROM USERS
                                  WHERE(USERS.USERNAME = %s)
                                  AND(USERS.EMAIL = %s)"""
                cursor.execute(statement, (username, email))
                currentuser_id = cursor.fetchone()
                query = """INSERT INTO SHAREDBOOKS(NAMEOFBOOK, LESSONNAME, LESSONCODE,TYPEOFSHARE,PRICE,USERID)
                                                                        VALUES (%s,%s,%s,%s,%s,%s)"""

                cursor.execute(query, (NameOfBook,LessonName,LessonCode,TypeOfShare,Price,currentuser_id))

                connection.commit()
        return render_template("sharedbooks_announcement.html")
    else:
        return render_template("sharedbooks_announcement.html")