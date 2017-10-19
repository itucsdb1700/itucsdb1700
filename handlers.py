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
from handler_operations.login import *
from handler_operations.sign_up import *
from handler_operations.restaurants import *

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

#@login_required
@site.route('/house_announcement',  methods=['GET', 'POST'])
def HousePage():
    return house_announcement_page()

@site.route('/', methods=['GET', 'POST'])
def LoginPage():
    return login_page()

@site.route('/sign_up', methods=['GET', 'POST'])
def SignUpPage():
  return sign_up_page()

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

@site.route('/restaurants', methods=['GET', 'POST'])
def RestaurantsPage():
    return restaurants_page()
