from flask import render_template, Blueprint, current_app, session, redirect, request
from flask.helpers import url_for
from flask_login import current_user, login_user, logout_user, login_required, LoginManager

import psycopg2 as dbapi2

from server import load_user
from user import User, get_user
from passlib.apps import custom_app_context as pwd_context
from datetime import datetime
import os.path

from classes.found_stuff_class import found_stuff

def found_stuff_page():
    if request.method == "POST":
        if 'userSearchButton' in request.form:  # if the search button is submitted
            session['search_username'] = request.form['usernameSearch']
            return redirect(url_for('site.SearchUserPage'))
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
                return redirect(url_for('site.FoundStuff'))
        elif formtype == "FoundSomethingUpdate":
            with dbapi2.connect(current_app.config['dsn']) as connection:
                cursor = connection.cursor()#prevented sql injection
                statement = """SELECT ID FROM USERS WHERE (USERS.USERNAME = %s) AND (USERS.EMAIL = %s)"""
                cursor.execute(statement, (username, email))
                founduser_id = cursor.fetchone()
                foundid = request.form['found-id']

                founddesc = request.form['FoundSomethingDescription']
                print("-", founddesc, "-\n")
                if not founddesc:
                    statement = """SELECT STUFFDESC FROM FOUNDSTUFF WHERE FOUNDSTUFF.ID = %s"""
                    cursor.execute(statement, foundid)
                    founddesc = cursor.fetchone()

                foundlocation = request.form['FoundSomethingCurrentLocation']
                print("-", foundlocation, "-\n")
                if not foundlocation:
                    statement = """SELECT CURRENTLOC FROM FOUNDSTUFF WHERE FOUNDSTUFF.ID = %s"""
                    cursor.execute(statement, foundid)
                    foundlocation = cursor.fetchone()

                founddate = request.form['FoundSomethingDate']
                if not founddate:
                    statement = """SELECT FINDINGDATE FROM FOUNDSTUFF WHERE FOUNDSTUFF.ID = %s"""
                    cursor.execute(statement,foundid)
                    founddate = cursor.fetchone()

                foundname = request.form['FoundSomethingFinderName']
                print("-", foundname, "-\n")
                if not foundname:
                    statement = """SELECT FOUNDERNAME FROM FOUNDSTUFF WHERE FOUNDSTUFF.ID = %s"""
                    cursor.execute(statement, foundid)
                    foundname = cursor.fetchone()

                foundmail = request.form['FoundSomethingFinderMail']
                print("-", foundmail, "-\n")
                if not foundmail:
                    statement = """SELECT FOUNDERMAIL FROM FOUNDSTUFF WHERE FOUNDSTUFF.ID = %s"""
                    cursor.execute(statement, foundid)
                    foundmail = cursor.fetchone()

                foundphone = request.form['FoundSomethingFinderPhone']
                print("-", foundphone, "-\n")
                if not foundphone:
                    statement = """SELECT FOUNDERPHONE FROM FOUNDSTUFF WHERE FOUNDSTUFF.ID = %s"""
                    cursor.execute(statement, foundid)
                    foundphone = cursor.fetchone()

                statement = """UPDATE FOUNDSTUFF SET STUFFDESC=%s, CURRENTLOC=%s, FINDINGDATE=%s, FOUNDERNAME=%s, FOUNDERMAIL=%s, FOUNDERPHONE=%s, USERID=%s WHERE FOUNDSTUFF.ID=%s"""
                cursor.execute(statement, (founddesc, foundlocation, founddate, foundname, foundmail, foundphone, founduser_id, foundid))
                connection.commit()
                return redirect(url_for('site.selected_found_stuff', foundId=foundid))
    else:
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """SELECT STUFFDESC, CURRENTLOC, FINDINGDATE, FOUNDERNAME, FOUNDERMAIL, FOUNDERPHONE, USERS.USERNAME, FOUNDSTUFF.ID FROM FOUNDSTUFF, USERS WHERE (FOUNDSTUFF.USERID = USERS.ID)"""
            cursor.execute(query)
            founditems = cursor.fetchall()
        return render_template('found_stuff.html', founditems=founditems)