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

from server import load_user

def lost_found_page():
    if request.method == "POST":
        formtype = request.form['form-name']
        if formtype == "LostSomething":
            lostdesc = request.form['LostSomethingDescription']
            lostlocation = request.form['LostSomethingPossibleLocation']
            lostdate = request.form['LostSomethingDate']
            lostowner = request.form['LostSomethingOwnerName']
            lostmail = request.form['LostSomethingOwnerMail']
            lostphone = request.form['LostSomethingOwnerPhone']

            with dbapi2.connect(current_app.config['dsn']) as connection:
                cursor = connection.cursor()#prevented sql injection
                query = """INSERT INTO LOSTSTUFF(STUFFDESC, POSSIBLELOC, POSSIBLEDATE, OWNERNAME, OWNERMAIL, OWNERPHONE) VALUES (%s, %s, %s, %s, %s, %s)"""
                cursor.execute(query, (lostdesc, lostlocation, lostdate, lostowner, lostmail, lostphone))
                connection.commit()
        else:
            founddesc = request.form['FoundSomethingDescription']
            foundlocation = request.form['FoundSomethingCurrentLocation']
            founddate = request.form['FoundSomethingDate']
            foundname = request.form['FoundSomethingFinderName']
            foundmail = request.form['FoundSomethingFinderMail']
            foundphone = request.form['FoundSomethingFinderPhone']

            with dbapi2.connect(current_app.config['dsn']) as connection:
                cursor = connection.cursor()#prevented sql injection
                query = """INSERT INTO FOUNDSTUFF(STUFFDESC, CURRENTLOC, FINDINGDATE, FOUNDERNAME, FOUNDERMAIL, FOUNDERPHONE) VALUES (%s, %s, %s, %s, %s, %s)"""
                cursor.execute(query, (founddesc, foundlocation, founddate, foundname, foundmail, foundphone))
                connection.commit()

        return render_template('lost_found.html')
    else:
        return render_template('lost_found.html')