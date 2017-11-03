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

def lost_stuff_page():
    if request.method == "POST":
        formtype = request.form['form-name']

        username = current_user.get_username()
        print(username) #use print to check whether the correct data is retrieved by checking the terminal
        password = current_user.get_password()
        print(password)
        email = current_user.get_email()
        print(email)

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
        return render_template('lost_stuff.html')
    else:
        return render_template('lost_stuff.html')