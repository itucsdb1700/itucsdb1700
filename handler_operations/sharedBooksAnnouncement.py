from flask import render_template, Blueprint,session
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

from classes.Sharing_Books_class import sharingBooksAnnouncement


def shared_Books_Announcement_Page():
    if request.method == "POST":
        if 'userSearchButton' in request.form:  # if the search button is submitted
            session['search_username'] = request.form['usernameSearch']
            return redirect(url_for('site.SearchUserPage'))

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

                sharedBooksAd = sharingBooksAnnouncement(NameOfBook,LessonName,LessonCode,TypeOfShare,Price,currentuser_id)
                query = """INSERT INTO SHAREDBOOKS(NAMEOFBOOK, LESSONNAME, LESSONCODE,TYPEOFSHARE,PRICE,USERID)
                                                                        VALUES (%s,%s,%s,%s,%s,%s)"""

                cursor.execute(query, (sharedBooksAd.NameOFSharingBooks,sharedBooksAd.LessonNameOfSharingBooks,
                                       sharedBooksAd.LessonCodeOfSharingBooks,sharedBooksAd.TypeOfSharingBooks,
                                       sharedBooksAd.PriceOFSharingBooks,sharedBooksAd.id_ownerOfSharingBooks))

                connection.commit()
            return redirect(url_for('site.SharedBooksAnnouncementPage'))
        elif formtype == "SharedBooksAnnouncementUpdate":
            with dbapi2.connect(current_app.config['dsn']) as connection:
                cursor = connection.cursor()  # prevented sql injection
                statement = """SELECT ID FROM USERS WHERE (USERS.USERNAME = %s) AND (USERS.EMAIL = %s)"""
                cursor.execute(statement, (username, email))
                sharingUser_id = cursor.fetchone()
                sharingBookid = request.form['sharingBooks-id']

                NameOfBook = request.form['InputNameOfSharedBook']
                if not NameOfBook:
                    statement = """SELECT NAMEOFBOOK FROM SHAREDBOOKS WHERE SHAREDBOOKS.ID = %s"""
                    cursor.execute(statement, sharingBookid)
                    NameOfBook = cursor.fetchone()

                LessonName = request.form['InputLessonNameOfShareBook']
                if not LessonName:
                    statement = """SELECT LESSONNAME FROM SHAREDBOOKS WHERE SHAREDBOOKS.ID = %s"""
                    cursor.execute(statement, sharingBookid)
                    LessonName = cursor.fetchone()

                LessonCode = request.form['InputLessonCodeOfShareBook']
                if not LessonCode:
                    statement = """SELECT LESSONCODE FROM SHAREDBOOKS WHERE SHAREDBOOKS.ID = %s"""
                    cursor.execute(statement, sharingBookid)
                    LessonCode = cursor.fetchone()

                TypeOfShare = request.form['InputTypeOfSharedBooks']
                if not TypeOfShare:
                    statement = """SELECT TYPEOFSHARE FROM SHAREDBOOKS WHERE SHAREDBOOKS.ID = %s"""
                    cursor.execute(statement, sharingBookid)
                    TypeOfShare = cursor.fetchone()

                Price = request.form['InputPriceOfShareBook']
                if not Price:
                    statement = """SELECT PRICE FROM SHAREDBOOKS WHERE SHAREDBOOKS.ID = %s"""
                    cursor.execute(statement, sharingBookid)
                    Price = cursor.fetchone()

                statement = """UPDATE SHAREDBOOKS SET NAMEOFBOOK=%s, LESSONNAME=%s, LESSONCODE=%s, TYPEOFSHARE=%s, PRICE=%s, USERID=%s WHERE SHAREDBOOKS.ID=%s"""
                cursor.execute(statement,(NameOfBook, LessonName, LessonCode, TypeOfShare, Price, sharingUser_id,sharingBookid))
                connection.commit()
                return redirect(url_for('site.selected_sharingBooks', id=sharingBookid))
    else:
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """SELECT NAMEOFBOOK,LESSONNAME,LESSONCODE,TYPEOFSHARE,PRICE,USERS.NAME,USERS.SURNAME,USERS.EMAIL,FACULTIES.FACULTYNAME,FACULTIES.FACULTYCODE,SHAREDBOOKS.ID FROM SHAREDBOOKS,USERS,FACULTIES
                              WHERE(SHAREDBOOKS.USERID = USERS.ID)
                              AND(USERS.FACULTYID = FACULTIES.ID)   
                    """
            cursor.execute(query)
            ALLSharingBooks = cursor.fetchall()
            return render_template("sharedbooks_announcement.html",ALLSharingBooks=ALLSharingBooks)