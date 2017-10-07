#this file contains the necessary handler functions
#instead of the app, blueprint is used for routing now

from flask import render_template, Blueprint
from datetime import datetime
from flask import current_app

from flask import redirect
from flask.helpers import url_for

from flask_login import login_required
from flask_login import current_user

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
  if current_user.is_authenticated:
    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """DROP TABLE IF EXISTS COUNTER"""
        cursor.execute(query)

        query = """CREATE TABLE COUNTER (N INTEGER)"""
        cursor.execute(query)

        query = """INSERT INTO COUNTER (N) VALUES (0)"""
        cursor.execute(query)

        connection.commit()

  return redirect(url_for('site.HomePage'))

@site.route('/')
def HomePage():
    now = datetime.now()
    return render_template('home.html', current_time=now.ctime())

@site.route('/house_announcement')
def HousePage():
    return render_template('house_announcement.html')   

@site.route('/lost_properties')
def PropertyPage():
    return render_template('lost_properties.html')

