from flask import render_template, Blueprint, current_app, session, redirect, request
from flask.helpers import url_for
from flask_login import current_user, login_user, logout_user, login_required, LoginManager

import psycopg2 as dbapi2

from server import load_user
from user import User, get_user
from passlib.apps import custom_app_context as pwd_context
from datetime import datetime
import os.path

from classes.lost_stuff_class import lost_stuff

def lost_stuff_page():
    if request.method == "POST":
        if 'userSearchButton' in request.form:  # if the search button is submitted
            session['search_username'] = request.form['usernameSearch']
            return redirect(url_for('site.SearchUserPage'))
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
                connection.commit()
            return redirect(url_for('site.LostStuff'))
        elif formtype == "LostSomethingUpdate":
            with dbapi2.connect(current_app.config['dsn']) as connection:
                cursor = connection.cursor()#prevented sql injection
                statement = """SELECT ID FROM USERS WHERE (USERS.USERNAME = %s) AND (USERS.EMAIL = %s)"""
                cursor.execute(statement, (username, email))
                lostuser_id = cursor.fetchone()
                lostid = request.form['lost-id']

                lostdesc = request.form['LostSomethingDescription']
                print("-", lostdesc, "-\n")
                if not lostdesc:
                    statement = """SELECT STUFFDESC FROM LOSTSTUFF WHERE LOSTSTUFF.ID = %s"""
                    cursor.execute(statement, lostid)
                    lostdesc = cursor.fetchone()

                lostlocation = request.form['LostSomethingPossibleLocation']
                print("-", lostlocation, "-\n")
                if not lostlocation:
                    statement = """SELECT POSSIBLELOC FROM LOSTSTUFF WHERE LOSTSTUFF.ID = %s"""
                    cursor.execute(statement, lostid)
                    lostlocation = cursor.fetchone()

                lostdate = request.form['LostSomethingDate']
                if not lostdate:
                    statement = """SELECT POSSIBLEDATE FROM LOSTSTUFF WHERE LOSTSTUFF.ID = %s"""
                    cursor.execute(statement,lostid)
                    lostdate = cursor.fetchone()

                lostname = request.form['LostSomethingOwnerName']
                print("-", lostname, "-\n")
                if not lostname:
                    statement = """SELECT OWNERNAME FROM LOSTSTUFF WHERE LOSTSTUFF.ID = %s"""
                    cursor.execute(statement, lostid)
                    lostname = cursor.fetchone()

                lostmail = request.form['LostSomethingOwnerMail']
                print("-", lostmail, "-\n")
                if not lostmail:
                    statement = """SELECT OWNERMAIL FROM LOSTSTUFF WHERE LOSTSTUFF.ID = %s"""
                    cursor.execute(statement, lostid)
                    lostmail = cursor.fetchone()

                lostphone = request.form['LostSomethingOwnerPhone']
                print("-", lostphone, "-\n")
                if not lostphone:
                    statement = """SELECT OWNERPHONE FROM LOSTSTUFF WHERE LOSTSTUFF.ID = %s"""
                    cursor.execute(statement, lostid)
                    lostphone = cursor.fetchone()

                statement = """UPDATE LOSTSTUFF SET STUFFDESC=%s, POSSIBLELOC=%s, POSSIBLEDATE=%s, OWNERNAME=%s, OWNERMAIL=%s, OWNERPHONE=%s, USERID=%s WHERE LOSTSTUFF.ID=%s"""
                cursor.execute(statement, (lostdesc, lostlocation, lostdate, lostname, lostmail, lostphone, lostuser_id, lostid))
                connection.commit()
                return redirect(url_for('site.selected_lost_stuff', lostId=lostid))
    else:
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """SELECT STUFFDESC, POSSIBLELOC, POSSIBLEDATE, OWNERNAME, OWNERMAIL, OWNERPHONE, USERS.USERNAME, LOSTSTUFF.ID FROM LOSTSTUFF, USERS WHERE (LOSTSTUFF.USERID = USERS.ID)"""
            cursor.execute(query)
            lostitems = cursor.fetchall()
        return render_template('lost_stuff.html', lostitems=lostitems)