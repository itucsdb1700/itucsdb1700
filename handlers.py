#this file contains the necessary handler functions
#instead of the app, blueprint is used for routing now

from flask import render_template, Blueprint
from flask import current_app
from datetime import datetime

from flask import redirect
from flask.helpers import url_for

from flask_login import login_required
from flask_login import current_user
from flask_login import LoginManager
from flask import request

import psycopg2 as dbapi2

site = Blueprint('site', __name__)

@site.route('/count')
def counter_page():
    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = "UPDATE COUNTER SET N = N + 1"
        cursor.execute(query)
        connection.commit()

        query = "SELECT N FROM COUNTER"
        cursor.execute(query)
        count = cursor.fetchone()[0]
    return "This page was accessed %d times." % count

@login_required
@site.route('/initdb')
def initialize_database():
  #if current_user.is_authenticated: This statement will stay as a comment until the admin user is created
  with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()

        #example counter table
        query = """DROP TABLE IF EXISTS COUNTER"""
        cursor.execute(query)

        query = """CREATE TABLE COUNTER (N INTEGER)"""
        cursor.execute(query)

        query = """INSERT INTO COUNTER (N) VALUES (0)"""
        cursor.execute(query)



        #creating table for lost stuff
        query = """DROP TABLE IF EXISTS LOSTSTUFF"""
        cursor.execute(query)

        query = """CREATE TABLE LOSTSTUFF (N INTEGER)"""
        cursor.execute(query)

        query = """INSERT INTO LOSTSTUFF (N) VALUES (0)"""
        cursor.execute(query)



        #creating table for found stuff
        query = """DROP TABLE IF EXISTS FOUNDSTUFF"""
        cursor.execute(query)

        query = """CREATE TABLE FOUNDSTUFF (N INTEGER)"""
        cursor.execute(query)

        query = """INSERT INTO FOUNDSTUFF (N) VALUES (0)"""
        cursor.execute(query)


        #create table for users
        query = """DROP TABLE IF EXISTS USERS"""  # DROP TABLE COMMANDS
        cursor.execute(query)

        query = """
              CREATE TABLE USERS (
              ID SERIAL PRIMARY KEY NOT NULL,
              USERNAME VARCHAR(30) NOT NULL,
              PASSWORD VARCHAR(30) NOT NULL,
              EMAIL VARCHAR(30) NOT NULL
        )"""
        cursor.execute(query)

        query = """INSERT INTO USERS(USERNAME, PASSWORD, EMAIL) VALUES ('hakansander', '123456', 'sander@hotmail.com' )"""
        cursor.execute(query)

        # create table for lost properties
        query = """DROP TABLE IF EXISTS LOSTSTUFF"""
        cursor.execute(query)

        query = """
              CREATE TABLE LOSTSTUFF (
              ID SERIAL PRIMARY KEY NOT NULL,
              STUFFDESC VARCHAR(300) NOT NULL, 
              POSSIBLELOC VARCHAR(50) NOT NULL,
              POSSIBLEDATE SMALLDATETIME NOT NULL,
              OWNERNAME VARCHAR(50) NOT NULL,
              OWNERMAIL VARCHAR(50) NOT NULL,
              OWNERPHONE VARCHAR(15) NOT NULL
        )"""
        cursor.execute(query)

        query = """INSERT INTO LOSTSTUFF(STUFFDESC, POSSIBLELOC, POSSIBLEDATE, OWNERNAME, OWNERMAIL, OWNERPHONE) VALUES ('KAYIP', 'MED', '2017-10-13 16:00:00', 'Sercan', 'sahanse@itu.edu.tr', '+905350000000')"""
        cursor.execute(query)

        # create table for found properties
        query = """DROP TABLE IF EXISTS FOUNDSTUFF"""
        cursor.execute(query)

        query = """
                      CREATE TABLE FOUNDSTUFF (
                      ID SERIAL PRIMARY KEY NOT NULL,
                      STUFFDESC VARCHAR(300) NOT NULL, 
                      CURRENTLOC VARCHAR(50) NOT NULL,
                      FINDINGDATE SMALLDATETIME NOT NULL,
                      FOUNDERNAME VARCHAR(50) NOT NULL,
                      FOUNDERMAIL VARCHAR(50) NOT NULL,
                      FOUNDERPHONE VARCHAR(15) NOT NULL
                )"""
        cursor.execute(query)

        query = """INSERT INTO FOUNDSTUFF(STUFFDESC, CURRENTLOC, FINDINGDATE, FOUNDERNAME, FOUNDERMAIL, FOUNDERPHONE) VALUES ('KAYIP', 'MED', '2017-10-13 16:00:00', 'Sercan', 'sahanse@itu.edu.tr', '+905350000000')"""
        cursor.execute(query)

        # creating table for game friends
        query = """DROP TABLE IF EXISTS GAMEFRIEND"""
        cursor.execute(query)

        query = """CREATE TABLE GAMEFRIEND(
                        ID SERIAL PRIMARY KEY,
                        NAME VARCHAR(80) NOT NULL,
                        TYPE VARCHAR(30) NOT NULL,
                        GAMEDATE DATE,
                        LOCATION VARCHAR(80),
                        PLAYERNUMBER INTEGER 
                )"""
        cursor.execute(query)

        # Insert an example row to the table GAMEFRIEND
        query = """INSERT INTO GAMEFRIEND (NAME, TYPE, GAMEDATE, LOCATION, PLAYERNUMBER) 
                                    VALUES('Batak', 'Table Game', '2017-10-13', 'MED', 4)"""
        cursor.execute(query)


        connection.commit()

  return redirect(url_for('site.HomePage'))

@site.route('/')
def LoginPage():
    now = datetime.now()
    return render_template('login.html', current_time=now.ctime())

@site.route('/home')
def HomePage():
    now = datetime.now()
    return render_template('home.html', current_time=now.ctime())

@site.route('/house_announcement')
def HousePage():
    return render_template('house_announcement.html')

@site.route('/sign_up', methods=['GET', 'POST'])
def SignUpPage():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    id = 1


    with dbapi2.connect(current_app.config['dsn']) as connection:
      cursor = connection.cursor()

      query = """
        INSERT INTO USERS (USERNAME, PASSWORD, EMAIL) 
        VALUES ('%s', '%s', '%s')""" % (
          username, password, email
        )

      cursor.execute(query)

      connection.commit()
    return render_template('home.html')

  else:
    return render_template('sign_up.html')




@site.route('/game_friends', methods=['GET', 'POST'])
def GameFriendPage():
    if request.method is 'POST':

        return render_template('home.html')

    else:
        return render_template('game_friends.html')



@site.route('/lost_found', methods=['GET', 'POST'])
def PropertyPage():
    if request.method is 'POST':

        return render_template('home.html')
    else:
        return render_template('lost_found.html')

