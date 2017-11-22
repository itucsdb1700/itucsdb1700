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

def searched_House_Announcement_Page():
    if request.method == "POST":
        if 'userSearchButton' in request.form:  # if the search button is submitted
            session['search_username'] = request.form['usernameSearch']
            return redirect(url_for('site.SearchUserPage'))

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
            Location = request.form['InputLocationOfSearchingHouse']
            MinRent = request.form['InputMinRentPriceOfSearchingHouse']
            MaxRent = request.form['InputMaxRentPriceOfSearchingHouse']
            Description = request.form['InputDescriptionOfSearchingHouse']

            with dbapi2.connect(current_app.config['dsn']) as connection:
                cursor = connection.cursor()
                statement = """SELECT ID FROM USERS
                                      WHERE(USERS.USERNAME = %s)
                                      AND(USERS.EMAIL = %s)"""
                cursor.execute(statement, (username,email))
                currentuser_id = cursor.fetchone()

                searchingHouseAd = searchingHouseAnnouncement(Location,MinRent,MaxRent,Description,currentuser_id)

                query = """INSERT INTO DATASEARCHEDHOUSE(LOCATION, MINRENTPRICE, MAXRENTPRICE,DESCRIPTION,USERID)
                                                        VALUES (%s,%s,%s,%s,%s)"""
                cursor.execute(query, (searchingHouseAd.LocationOfSearchingHouse, searchingHouseAd.MinRentPriceOfSearchingHouse, searchingHouseAd.MaxRentPriceOfSearchingHouse,searchingHouseAd.DescriptionOfSearchingHouse,searchingHouseAd.id_ownerOfSearchingHouseAnnouncement))
                query = """SELECT  LOCATION,MINRENTPRICE,MAXRENTPRICE,DESCRIPTION,USERS.NAME,USERS.SURNAME,USERS.EMAIL,FACULTIES.FACULTYNAME,FACULTIES.FACULTYCODE FROM DATASEARCHEDHOUSE,USERS,FACULTIES
                                              WHERE(DATASEARCHEDHOUSE.USERID = USERS.ID)
                                              AND(USERS.FACULTYID = FACULTIES.ID)
                                    """
                cursor.execute(query)
                ALLSearchedHouse = cursor.fetchall()
                connection.commit()

        return render_template("searchedhouse_announcement.html",ALLSearchedHouse =ALLSearchedHouse)
    else:
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """SELECT  LOCATION,MINRENTPRICE,MAXRENTPRICE,DESCRIPTION,USERS.NAME,USERS.SURNAME,USERS.EMAIL,FACULTIES.FACULTYNAME,FACULTIES.FACULTYCODE FROM DATASEARCHEDHOUSE,USERS,FACULTIES
                              WHERE(DATASEARCHEDHOUSE.USERID = USERS.ID)
                              AND(USERS.FACULTYID = FACULTIES.ID)
                    """
            cursor.execute(query)
            ALLSearchedHouse = cursor.fetchall()
        return render_template('searchedhouse_announcement.html', ALLSearchedHouse=ALLSearchedHouse)