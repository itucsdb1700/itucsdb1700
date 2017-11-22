from flask import render_template, Blueprint, current_app, session, redirect, request
from flask.helpers import url_for
from flask_login import current_user, login_user, logout_user, login_required, LoginManager

import psycopg2 as dbapi2

from server import load_user
from user import User, get_user
from passlib.apps import custom_app_context as pwd_context
from datetime import datetime
import os.path

from classes.Searching_House_class import searchingHouseAnnouncement
def searched_House_Announcement_For_Profile_Page():
    username = current_user.get_username()
    email = current_user.get_email()

    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        statement = """SELECT ID FROM USERS
                              WHERE(USERS.USERNAME = %s)
                              AND(USERS.EMAIL = %s)"""
        cursor.execute(statement, (username, email))
        currentuser_id = cursor.fetchone()

        query = """SELECT  LOCATION,MINRENTPRICE,MAXRENTPRICE,DESCRIPTION,ID FROM DATASEARCHEDHOUSE
                                      WHERE(DATASEARCHEDHOUSE.USERID = %s)
                            """
        cursor.execute(query,(currentuser_id))
        AllYourSearchedHouseAnnouncement = cursor.fetchall()
        connection.commit()

    return render_template("profile_searchedhouse_announcement.html",AllYourSearchedHouseAnnouncement = AllYourSearchedHouseAnnouncement)