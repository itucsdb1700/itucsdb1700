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
        query = """DROP TABLE IF EXISTS USERS"""  # DROP TABLE COMMANDS
        cursor.execute(query)
        query = """DROP TABLE IF EXISTS LOSTSTUFF"""
        cursor.execute(query)
        query = """DROP TABLE IF EXISTS FOUNDSTUFF"""
        cursor.execute(query)
        query = """DROP TABLE IF EXISTS GAMEFRIEND"""
        cursor.execute(query)
        query = """DROP TABLE IF EXISTS SHARINGHOUSE CASCADE """
        cursor.execute(query)
        query = """DROP TABLE IF EXISTS PERSONOFSHAREHOUSE CASCADE """
        cursor.execute(query)
        query = """DROP TABLE IF EXISTS DATASHAREDHOUSE CASCADE """
        cursor.execute(query)
        query = """DROP TABLE IF EXISTS FINDINGHOUSE CASCADE """
        cursor.execute(query)
        query = """DROP TABLE IF EXISTS PERSONOFSEARCHHOUSE CASCADE """
        cursor.execute(query)
        query = """DROP TABLE IF EXISTS DATASEARCHEDHOUSE CASCADE """
        cursor.execute(query)

        query = """CREATE TABLE COUNTER (N INTEGER)"""
        cursor.execute(query)

        query = """INSERT INTO COUNTER (N) VALUES (0)"""
        cursor.execute(query)


        #create table for users


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
        query = """
              CREATE TABLE LOSTSTUFF (
              ID SERIAL PRIMARY KEY NOT NULL,
              STUFFDESC VARCHAR(300) NOT NULL, 
              POSSIBLELOC VARCHAR(50) NOT NULL,
              POSSIBLEDATE DATE NOT NULL,
              OWNERNAME VARCHAR(50) NOT NULL,
              OWNERMAIL VARCHAR(50) NOT NULL,
              OWNERPHONE VARCHAR(15) NOT NULL
        )"""
        cursor.execute(query)

        query = """INSERT INTO LOSTSTUFF(STUFFDESC, POSSIBLELOC, POSSIBLEDATE, OWNERNAME, OWNERMAIL, OWNERPHONE) VALUES ('KAYIP', 'MED', '2017-10-13 16:00:00', 'Sercan', 'sahanse@itu.edu.tr', '+905350000000')"""
        cursor.execute(query)

        # create table for found properties


        query = """
              CREATE TABLE FOUNDSTUFF (
              ID SERIAL PRIMARY KEY NOT NULL,
              STUFFDESC VARCHAR(300) NOT NULL, 
              CURRENTLOC VARCHAR(50) NOT NULL,
              FINDINGDATE DATE NOT NULL,
              FOUNDERNAME VARCHAR(50) NOT NULL,
              FOUNDERMAIL VARCHAR(50) NOT NULL,
              FOUNDERPHONE VARCHAR(15) NOT NULL
        )"""
        cursor.execute(query)

        query = """INSERT INTO FOUNDSTUFF(STUFFDESC, CURRENTLOC, FINDINGDATE, FOUNDERNAME, FOUNDERMAIL, FOUNDERPHONE) VALUES ('KAYIP', 'MED', '2017-10-13 16:00:00', 'Sercan', 'sahanse@itu.edu.tr', '+905350000000')"""
        cursor.execute(query)


        # creating table for game friends


        query = """
                      CREATE TABLE GAMEFRIEND(
                      ID SERIAL PRIMARY KEY,
                      NAME VARCHAR(80) NOT NULL,
                      TYPE VARCHAR(30) NOT NULL,
                      GAMEDATE DATE,
                      LOCATION VARCHAR(80),
                      PLAYERNUMBER INTEGER,
                      DESCRIPTION VARCHAR(120)
                )"""
        cursor.execute(query)

        # Insert an example row to the table GAMEFRIEND
        query = """INSERT INTO GAMEFRIEND (NAME, TYPE, GAMEDATE, LOCATION, PLAYERNUMBER, DESCRIPTION) 
                                            VALUES('Batak', 'Table Game', '2017-10-13', 'MED', 4, 'Come with your couple')"""
        cursor.execute(query)


        # creating table for shared house information


        query = """
              CREATE TABLE DATASHAREDHOUSE(
              ID SERIAL PRIMARY KEY NOT NULL,
              LOCATION VARCHAR(80) NOT NULL,
              RENTPRICE INTEGER NOT NULL,
              NUMBEROFPEOPLE INTEGER NOT NULL,
              NUMBEROFROOM VARCHAR (3) NOT NULL,
              DESCRIPTION VARCHAR (300) NOT NULL,
              GENDER VARCHAR (6) NOT NULL  
        )"""
        cursor.execute(query)

        query = """INSERT INTO DATASHAREDHOUSE(LOCATION, RENTPRICE, NUMBEROFPEOPLE,NUMBEROFROOM,DESCRIPTION,GENDER) VALUES ('Levent', '1500', '2','3+1','aa','Male' )"""
        cursor.execute(query)

        ###########################################
        # creating table for person who share house


        query = """
              CREATE TABLE PERSONOFSHAREHOUSE(
              ID SERIAL PRIMARY KEY NOT NULL,
              NAME VARCHAR (50),
              GENDER VARCHAR (6),
              DEPARTMENT VARCHAR (30),
              TELNO VARCHAR (20)
        )"""
        cursor.execute(query)

        query = """INSERT INTO PERSONOFSHAREHOUSE(NAME, GENDER, DEPARTMENT,TELNO) VALUES ('Adil Furkan Ekici', 'Male', 'Computer Eng.', '05420000000')"""
        cursor.execute(query)

        # creating table for share house and housemate information


        query = """
               CREATE TABLE SHARINGHOUSE(
               ID SERIAL PRIMARY KEY NOT NULL,
               PERSONOFSHAREID INTEGER REFERENCES PERSONOFSHAREHOUSE(ID),
               SHAREDHOUSEID INTEGER REFERENCES DATASHAREDHOUSE(ID)   
         )"""
        cursor.execute(query)

        # creating table for criteria of searched house information


        query = """
              CREATE TABLE DATASEARCHEDHOUSE(
              ID SERIAL PRIMARY KEY NOT NULL,
              LOCATION VARCHAR(80) NOT NULL,
              MINRENTPRICE INTEGER NOT NULL,
              MAXRENTPRICE INTEGER NOT NULL,
              NUMBEROFROOM VARCHAR (3) NOT NULL,
              DESCRIPTION VARCHAR (300) NOT NULL,
              GENDER VARCHAR (6) NOT NULL  
        )"""
        cursor.execute(query)

        query = """INSERT INTO DATASEARCHEDHOUSE(LOCATION, MINRENTPRICE, MAXRENTPRICE,NUMBEROFROOM,DESCRIPTION,GENDER) VALUES ('Levent', '300', '500','3+1','aa','Male' )"""
        cursor.execute(query)

        # creating table for person who share house


        query = """
                      CREATE TABLE PERSONOFSEARCHHOUSE(
                      ID SERIAL PRIMARY KEY NOT NULL,
                      NAME VARCHAR (50),
                      GENDER VARCHAR (6),
                      DEPARTMENT VARCHAR (30),
                      TELNO VARCHAR (20)
                )"""
        cursor.execute(query)

        query = """INSERT INTO PERSONOFSHAREHOUSE(NAME, GENDER, DEPARTMENT,TELNO) VALUES ('Adil Furkan Ekici', 'Male', 'Computer Eng.', '05420000000')"""
        cursor.execute(query)

        # creating table for searched house criteria and person of searching house information

        query = """
               CREATE TABLE FINDINGHOUSE(
               ID SERIAL PRIMARY KEY NOT NULL,
               PERSONOFSEARCHID INTEGER REFERENCES PERSONOFSEARCHHOUSE(ID),
               SEARCHEDHOUSEID INTEGER REFERENCES DATASEARCHEDHOUSE(ID)   
         )"""
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
            VALUES ('%s', '%s', '%s')""" % (username, password, email
        )

      cursor.execute(query)

      connection.commit()
    return render_template('home.html')

  else:
    return render_template('sign_up.html')




@site.route('/game_friends', methods=['GET', 'POST'])
def GameFriendPage():
    if request.method == 'POST':
        gameName = request.form['InputGameName']
        gameType = request.form['InputGameType']
        if not request.form['GamePlayerNo']:
            playerNum = None
        else:
            playerNum = int(request.form['GamePlayerNo'])
        gameDate = request.form['InputGameDate']
        gameLoc = request.form['InputGameLocation']
        gameDesc = request.form['GameDescription']

        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()

            query = """INSERT INTO GAMEFRIEND (NAME, TYPE, GAMEDATE, LOCATION, PLAYERNUMBER, DESCRIPTION) 
                                                VALUES('%s', '%s', '%s', '%s', '%d', '%s')""" % (
                gameName, gameType, gameDate, gameLoc, playerNum, gameDesc )

            cursor.execute(query)
            connection.commit()

        return render_template('game_friends.html')

    else:
        return render_template('game_friends.html')



@site.route('/lost_found', methods=['GET', 'POST'])
def PropertyPage():
    if request.method is 'POST':

        return render_template('home.html')
    else:
        return render_template('lost_found.html')

