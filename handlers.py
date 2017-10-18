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
import os.path

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
        with connection.cursor() as cursor:
            with site.open_resource('script.sql', 'r') as file:
                statements = file.read()
                cursor.execute(statements)
            #scriptFile = open("script.sql", "r")
            #cursor.execute(scriptFile.read())

  return redirect(url_for('site.HomePage'))


@site.route('/home')
def HomePage():
    now = datetime.now()
    return render_template('home.html', current_time=now.ctime())

@site.route('/house_announcement',  methods=['GET', 'POST'])
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
                                                VALUES('%s', '%s', '%s', '%s', '%s', '%s')""" % (LocationOfSharingHouse, RentPriceOfSharingHouse, numberOfPeopleInHouse, NumberOfRoomOfSharingHouse, DescriptionOfSharingHouse,  GenderforSharingHouse)

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

