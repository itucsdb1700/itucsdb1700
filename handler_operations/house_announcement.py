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

site = Blueprint('site', __name__)

from server import load_user

def house_announcement_page():
    if request.method == "POST":
        formtype = request.form['form-name']
        if formtype == "SharedHouseAnnouncement":
            LocationOfSharingHouse = request.form['InputLocationOfSharingHouse']
            RentPriceOfSharingHouse = request.form['InputRentPriceOfSharingHouse']
            numberOfPeopleInHouse = request.form['InputnumberOfPeopleInHouse']
            GenderforSharingHouse = request.form['InputGenderforSharingHouse']
            NumberOfRoomOfSharingHouse = request.form['InputNumberOfRoomforSharingHouse']
            DescriptionOfSharingHouse = request.form['InputGenderforSharingHouse']

            with dbapi2.connect(current_app.config['dsn']) as connection:
                cursor = connection.cursor()#prevented sql injection
                query = """INSERT INTO DATASHAREDHOUSE(LOCATION, RENTPRICE, NUMBEROFPEOPLE, NUMBEROFROOM, DESCRIPTION, GENDER) VALUES (%s, %s, %s, %s, %s, %s)"""
                cursor.execute(query, (LocationOfSharingHouse, RentPriceOfSharingHouse, numberOfPeopleInHouse,NumberOfRoomOfSharingHouse, GenderforSharingHouse, DescriptionOfSharingHouse))
                connection.commit()
        if formtype == "SearchedHouseAnnouncement":
            LocationOfSearchingHouse = request.form['InputLocationOfSearchingHouse']
            MinRentPriceOfSearchingHouse = request.form['InputMinRentPriceOfSearchingHouse']
            MaxRentPriceOfSearchingHouse = request.form['InputMaxRentPriceOfSearchingHouse']
            DescriptionOfSearchingHouse = request.form['InputDescriptionOfSearchingHouse']
            GenderforSearchingHouse = request.form['InputGenderforSearchingHouse']

            with dbapi2.connect(current_app.config['dsn']) as connection:
                cursor = connection.cursor()

                query = """INSERT INTO DATASEARCHEDHOUSE(LOCATION, MINRENTPRICE, MAXRENTPRICE,DESCRIPTION,GENDER)
                                                        VALUES (%s,%s,%s,%s,%s,%s)"""

                cursor.execute(query, (LocationOfSearchingHouse, MinRentPriceOfSearchingHouse, MaxRentPriceOfSearchingHouse,DescriptionOfSearchingHouse,GenderforSearchingHouse))
                connection.commit()

        return render_template('house_announcement.html')
    else:
        return render_template('house_announcement.html')
