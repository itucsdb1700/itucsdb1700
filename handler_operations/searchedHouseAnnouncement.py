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

def searched_House_Announcement_Page():
    if request.method == "POST":
        formtype = request.form['form-name']

        username = current_user.get_username()
        print(username)  # use print to check whether the correct data is retrieved by checking the terminal
        password = current_user.get_password()
        print(password)
        email = current_user.get_email()
        print(email)
        name = current_user.get_name()
        print(name)
        surname = current_user.get_surname()
        print(surname)
        faculty_id = current_user.get_faculty_id()
        print(faculty_id)
        if formtype == "SearchingHouseAnnouncement":
            LocationOfSearchingHouse = request.form['InputLocationOfSearchingHouse']
            MinRentPriceOfSearchingHouse = request.form['InputMinRentPriceOfSearchingHouse']
            MaxRentPriceOfSearchingHouse = request.form['InputMaxRentPriceOfSearchingHouse']
            DescriptionOfSearchingHouse = request.form['InputDescriptionOfSearchingHouse']

            with dbapi2.connect(current_app.config['dsn']) as connection:
                cursor = connection.cursor()
                statement = """SELECT ID FROM USERS
                                      WHERE(USERS.USERNAME = %s)
                                      AND(USERS.EMAIL = %s)"""
                cursor.execute(statement, (username,email))
                currentuser_id = cursor.fetchone()

                query = """INSERT INTO DATASEARCHEDHOUSE(LOCATION, MINRENTPRICE, MAXRENTPRICE,DESCRIPTION,USERID)
                                                        VALUES (%s,%s,%s,%s,%s)"""
                cursor.execute(query, (LocationOfSearchingHouse, MinRentPriceOfSearchingHouse, MaxRentPriceOfSearchingHouse,DescriptionOfSearchingHouse,currentuser_id))
                connection.commit()

        return render_template("searchedhouse_announcement.html")
    else:
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """SELECT  DATASEARCHEDHOUSE.ID ,LOCATION,MINRENTPRICE,MAXRENTPRICE,DESCRIPTION,USERS.NAME,USERS.SURNAME FROM DATASEARCHEDHOUSE,USERS
                              WHERE(DATASEARCHEDHOUSE.USERID = USERS.ID)
                    """
            cursor.execute(query)
            searchedHouse = cursor.fetchall()
        return render_template('searchedhouse_announcement.html', searchedHouse=searchedHouse)