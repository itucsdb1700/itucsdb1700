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
import user


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
  if current_user.is_authenticated:
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
        query = """
              CREATE TABLE USERS (
              USERNAME VARCHAR(30) NOT NULL
              PASSWORD VARCHAR(30) NOT NULL 
              ID INT PRIMARY KEY NOT NULL
        )"""
        cursor.execute(query)

        query = """INSERT INTO USERS(USERNAME, PASSWORD) VALUES ('hakansander', '123456' )"""
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

@site.route('/lost_properties')
def PropertyPage():
    return render_template('lost_properties.html')

