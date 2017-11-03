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

from classes.Sharing_House_class import sharingHouseAnnouncement

def share_MyHouse_Announcement_Page():
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

        if formtype == "SharedHouseAnnouncement":
            Location = request.form['InputLocationOfSharingHouse']
            RentPrice = request.form['InputRentPriceOfSharingHouse']
            NumberOfPeople = request.form['InputnumberOfPeopleInHouse']
            NumberOfRoom = request.form['InputNumberOfRoomforSharingHouse']
            Description = request.form['InputDescriptionOfSharingHouse']

            with dbapi2.connect(current_app.config['dsn']) as connection:
                cursor = connection.cursor()#prevented sql injection
                statement = """SELECT ID FROM USERS WHERE(USERS.USERNAME = %s) AND(USERS.EMAIL = %s)"""
                cursor.execute(statement, (username,email))
                currentuser_id = cursor.fetchone()

                sharingHouseAd = sharingHouseAnnouncement(Location,RentPrice,NumberOfPeople,NumberOfRoom,Description,currentuser_id)


                query = """INSERT INTO DATASHAREDHOUSE(LOCATION, RENTPRICE, NUMBEROFPEOPLE, NUMBEROFROOM, DESCRIPTION, USERID) VALUES (%s, %s, %s, %s, %s, %s)"""
                cursor.execute(query, (sharingHouseAd.LocationOfSharingHouse, sharingHouseAd.RentPriceOfSharingHouse, sharingHouseAd.NumberOfPeopleInSharingHouse,
                                       sharingHouseAd.NumberOfSharingHouseRoom, sharingHouseAd.DescriptionOfSharingHouse,sharingHouseAd.id_ownerOfSharingHouseAnnouncement))

                connection.commit()

        return render_template("sharedmyhouse_announcement.html")

    else:
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """SELECT DATASHAREDHOUSE.ID ,LOCATION,RENTPRICE,NUMBEROFPEOPLE,NUMBEROFROOM,DESCRIPTION,USERS.NAME,USERS.SURNAME FROM DATASHAREDHOUSE,USERS
                              WHERE(DATASHAREDHOUSE.USERID = USERS.ID)
                    """
            cursor.execute(query)
            ALLSharingHouse = cursor.fetchall()
        return render_template('sharedmyhouse_announcement.html', ALLSharingHouse=ALLSharingHouse)