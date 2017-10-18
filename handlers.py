#this file contains the necessary handler functions
#instead of the app, blueprint is used for routing now

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

site = Blueprint('site', __name__)
from server import load_user
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

#@login_required
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
        query = """DROP TABLE IF EXISTS RESTAURANTS"""
        cursor.execute(query)
        query = """DROP TABLE IF EXISTS CAMPUSLOCATIONS"""
        cursor.execute(query)
        query = """DROP TABLE IF EXISTS FOODTYPES"""
        cursor.execute(query)
        query = """DROP TABLE IF EXISTS SERVICETYPES"""
        cursor.execute(query)
        query = """DROP TABLE IF EXISTS RESTAURANTMENUS"""
        cursor.execute(query)
        query = """DROP TABLE IF EXISTS RESTAURANTPOINTS"""
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
              PASSWORD VARCHAR(500) NOT NULL,
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

        query = """INSERT INTO LOSTSTUFF(STUFFDESC, POSSIBLELOC, POSSIBLEDATE, OWNERNAME, OWNERMAIL, OWNERPHONE) VALUES ('KAYIP', 'MED', '2017-10-13', 'Sercan', 'sahanse@itu.edu.tr', '+905350000000')"""
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

        query = """INSERT INTO FOUNDSTUFF(STUFFDESC, CURRENTLOC, FINDINGDATE, FOUNDERNAME, FOUNDERMAIL, FOUNDERPHONE) VALUES ('KAYIP', 'MED', '2017-10-13', 'Sercan', 'sahanse@itu.edu.tr', '+905350000000')"""
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



        #Create tables related to restaurants page
        #FOREIGN KEYS and REFERENCES will be added later..

        query = """
                CREATE TABLE RESTAURANTS (
                  ID SERIAL PRIMARY KEY NOT NULL,
                  LOCATION INTEGER NOT NULL,
                  MENUTYPE INTEGER NOT NULL,
                  RESTAURANTPOINT INTEGER NOT NULL,
                  PRICEBALANCE INTEGER NOT NULL,
                  OPENINGTIME TIME  NOT NULL,
                  CLOSINGTIME TIME NOT NULL
        )"""
        cursor.execute(query)

        query = """
                CREATE TABLE CAMPUSLOCATIONS (
                  ID SERIAL PRIMARY KEY NOT NULL,
                  CAMPUSNAME  VARCHAR(50) NOT NULL,
                  CAMPUSDISTRICT VARCHAR(50) NOT NULL
        )"""
        cursor.execute(query)

        query = """
                CREATE TABLE FOODTYPES (
                  ID SERIAL PRIMARY KEY NOT NULL,
                  FOODTYPENAME  VARCHAR(50) NOT NULL
        )"""
        cursor.execute(query)

        query = """
                CREATE TABLE SERVICETYPES (
                  ID SERIAL PRIMARY KEY NOT NULL,
                  SERVICETYPE  VARCHAR(50) NOT NULL
        )"""
        cursor.execute(query)

        query = """
                CREATE TABLE RESTAURANTMENUS (
                  ID SERIAL PRIMARY KEY NOT NULL,
                  FOODTYPE  INTEGER NOT NULL,
                  FOODNAME VARCHAR(40) NOT NULL,
                  FOODPRICE FLOAT NOT NULL
        )"""
        cursor.execute(query)

        query = """
                        CREATE TABLE RESTAURANTPOINTS (
                          RESTAURANTID SERIAL PRIMARY KEY NOT NULL,
                          TOTALPOINTS  INTEGER NOT NULL
          )"""
        cursor.execute(query)

        connection.commit()

  return redirect(url_for('site.HomePage'))

@site.route('/home')
def HomePage():
    now = datetime.now()
    return render_template('home.html', current_time=now.ctime())

@site.route('/house_announcement')
def HousePage():
    if request.method == 'POST'and request.form["InputLocationOfSharingHouse"] != None:
        LocationOfSharingHouse = request.form['InputLocationOfSharingHouse']
        RentPriceOfSharingHouse = request.form['InputRentPriceOfSharingHouse']
        numberOfPeopleInHouse = request.form['InputnumberOfPeopleInHouse']
        GenderforSharingHouse = request.form['InputGenderforSharingHouse']
        NumberOfRoomOfSharingHouse = request.form['InputNumberOfRoomforSharingHouse']
        DescriptionOfSharingHouse = request.form['InputDescriptionOfSharingHouse']
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()

            query = """INSERT INTO DATASHAREDHOUSE(LOCATION, RENTPRICE, NUMBEROFPEOPLE,NUMBEROFROOM,DESCRIPTION,GENDER) 
                                                VALUES('%s', '%s', '%s', '%s', '%s', '%s')""" % (LocationOfSharingHouse, RentPriceOfSharingHouse, numberOfPeopleInHouse, GenderforSharingHouse, NumberOfRoomOfSharingHouse, DescriptionOfSharingHouse )

            cursor.execute(query)
            connection.commit()

        return render_template('house_announcement.html')
    else:
        return render_template('house_announcement.html')
####and request.form["InputLocationOfSharingHouse"] != None
@site.route('/', methods=['GET', 'POST'])
def LoginPage():
    now = datetime.now()
    if request.method == 'POST':
      login_email = request.form['login_email']
      #print( "%s" % login_email)
      login_password = request.form['login_password']
      hashed_login_password = pwd_context.encrypt(login_password)

      with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        statement = """SELECT USERNAME FROM USERS WHERE USERNAME = %s"""
        cursor.execute(statement, [login_email])
        db_username = cursor.fetchone()

        if db_username is not None: #check whether the user exists
          print('%s' % db_username)
          user = load_user(db_username);
          login_user(user);
          print("%s" % user.username)
          #print('%s %s' % db_username[0][0], db_username[0][1] ) if the fetchall method is used debug using this line


      return render_template('home.html', current_time=now.ctime())
    else:
      return render_template('login.html', current_time=now.ctime())

@site.route('/sign_up', methods=['GET', 'POST'])
def SignUpPage():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    hashed_password = pwd_context.encrypt(password)
    email = request.form['email']
    id = 1


    with dbapi2.connect(current_app.config['dsn']) as connection:
      cursor = connection.cursor()

      query = """
            INSERT INTO USERS (USERNAME, PASSWORD, EMAIL) 
            VALUES ('%s', '%s', '%s')""" % (username, hashed_password, email)

      cursor.execute(query)

      connection.commit()
    return render_template('home.html')

  else:
    return render_template('sign_up.html')



#@login_required
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
                                                VALUES('%s', '%s', '%s', '%s', '%d', '%s')""" % (gameName, gameType, gameDate, gameLoc, playerNum, gameDesc )

            cursor.execute(query)
            connection.commit()

        return render_template('game_friends.html')

    else:
        return render_template('game_friends.html')



@site.route('/lost_found', methods=['GET', 'POST'])
def PropertyPage():
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
                cursor = connection.cursor()
                query = """INSERT INTO LOSTSTUFF(STUFFDESC, POSSIBLELOC, POSSIBLEDATE, OWNERNAME, OWNERMAIL, OWNERPHONE) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')""" % (lostdesc, lostlocation, lostdate, lostowner, lostmail, lostphone)
                cursor.execute(query)
                connection.commit()
        else:
            founddesc = request.form['FoundSomethingDescription']
            foundlocation = request.form['FoundSomethingCurrentLocation']
            founddate = request.form['FoundSomethingDate']
            foundname = request.form['FoundSomethingFinderName']
            foundmail = request.form['FoundSomethingFinderMail']
            foundphone = request.form['FoundSomethingFinderPhone']

            with dbapi2.connect(current_app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """INSERT INTO FOUNDSTUFF(STUFFDESC, CURRENTLOC, FINDINGDATE, FOUNDERNAME, FOUNDERMAIL, FOUNDERPHONE) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')""" % (founddesc, foundlocation, founddate, foundname, foundmail, foundphone)
                cursor.execute(query)
                connection.commit()

        return render_template('lost_found.html')
    else:
        return render_template('lost_found.html')

