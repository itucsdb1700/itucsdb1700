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

from classes.found_stuff_class import found_stuff

from server import load_user

def found_stuff_page():
    if request.method == "POST":
        formtype = request.form['form-name']

        username = current_user.get_username()
        #print(username)  # use print to check whether the correct data is retrieved by checking the terminal
        email = current_user.get_email()
        #print(email)
        name = current_user.get_name()
        #print(name)
        surname = current_user.get_surname()
        #print(surname)

        if formtype == "FoundSomething":
            founddesc = request.form['FoundSomethingDescription']
            foundlocation = request.form['FoundSomethingCurrentLocation']
            founddate = request.form['FoundSomethingDate']
            foundname = request.form['FoundSomethingFinderName']
            if not foundname:
                seq = {name, surname}
                foundname = " ".join(seq)
            foundmail = request.form['FoundSomethingFinderMail']
            if not foundmail:
                foundmail = email
            foundphone = request.form['FoundSomethingFinderPhone']

            with dbapi2.connect(current_app.config['dsn']) as connection:
                cursor = connection.cursor()#prevented sql injection
                statement = """SELECT ID FROM USERS WHERE (USERS.USERNAME = %s) AND (USERS.EMAIL = %s)"""
                cursor.execute(statement, (username, email))
                founduser_id = cursor.fetchone()

                found = found_stuff(founddesc, foundlocation, founddate, foundname, foundmail, foundphone, founduser_id)
                query = """INSERT INTO FOUNDSTUFF(STUFFDESC, CURRENTLOC, FINDINGDATE, FOUNDERNAME, FOUNDERMAIL, FOUNDERPHONE, USERID) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
                cursor.execute(query, (found.description, found.location, found.date, found.name, found.mail, found.phone, found.user_id))
                connection.commit()
        return render_template('found_stuff.html')
    else:
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """SELECT STUFFDESC, CURRENTLOC, FINDINGDATE, FOUNDERNAME FROM FOUNDSTUFF"""
            cursor.execute(query)
            founditems = cursor.fetchall()
        return render_template('found_stuff.html', founditems=founditems)