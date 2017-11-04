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

from classes.lost_stuff_class import lost_stuff

from server import load_user

def lost_stuff_page():
    if request.method == "POST":
        formtype = request.form['form-name']

        username = current_user.get_username()
        #print(username) #use print to check whether the correct data is retrieved by checking the terminal
        email = current_user.get_email()
        #print(email)
        name = current_user.get_name()
        #print(name)
        surname = current_user.get_surname()
        #print(surname)

        if formtype == "LostSomething":
            lostdesc = request.form['LostSomethingDescription']
            lostlocation = request.form['LostSomethingPossibleLocation']
            lostdate = request.form['LostSomethingDate']
            lostownername = request.form['LostSomethingOwnerName']
            if not lostownername:
                seq = {name, surname}
                lostownername = " ".join(seq)
            lostmail = request.form['LostSomethingOwnerMail']
            if not lostmail:
                lostmail = email
            lostphone = request.form['LostSomethingOwnerPhone']

            with dbapi2.connect(current_app.config['dsn']) as connection:
                cursor = connection.cursor()#prevented sql injection
                statement = """SELECT ID FROM USERS WHERE (USERS.USERNAME = %s) AND (USERS.EMAIL = %s)"""
                cursor.execute(statement, (username, email))
                lostuser_id = cursor.fetchone()

                lost = lost_stuff(lostdesc, lostlocation, lostdate, lostownername, lostmail, lostphone, lostuser_id)
                query = """INSERT INTO LOSTSTUFF(STUFFDESC, POSSIBLELOC, POSSIBLEDATE, OWNERNAME, OWNERMAIL, OWNERPHONE, USERID) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
                cursor.execute(query, (lost.description, lost.location, lost.date, lost.ownername, lost.mail, lost.phone, lost.user_id))
                query = """SELECT STUFFDESC, POSSIBLELOC, POSSIBLEDATE, OWNERNAME FROM LOSTSTUFF"""
                cursor.execute(query)
                lostitems = cursor.fetchall()
                connection.commit()
            return render_template('lost_stuff.html', lostitems=lostitems)
    else:
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """SELECT STUFFDESC, POSSIBLELOC, POSSIBLEDATE, OWNERNAME FROM LOSTSTUFF"""
            cursor.execute(query)
            lostitems = cursor.fetchall()
        return render_template('lost_stuff.html', lostitems=lostitems)