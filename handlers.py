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



from handler_operations.lost_found import *
from handler_operations.house_announcement import *

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
    return house_announcement_page()


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
    return lost_found_page()

