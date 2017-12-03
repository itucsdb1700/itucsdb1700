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

from server import load_user

def sign_up_validation(form):
    form.data = {}
    form.errors = {}

    if len(form['email'].strip()) == 0:
        form.errors['email'] = 'Email can not be left blank!'
    else:
        form.data['email'] = form['email']

    if len(form['username'].strip()) == 0:
        form.errors['username'] = 'Username can not be left blank!'
    else:
        form.data['username'] = form['username']

    username = form['username']
    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """
        SELECT COUNT(USERS.USERNAME)
          FROM USERS
          WHERE USERS.USERNAME = %s
      """
        cursor.execute(query, [username])
        user_flag = cursor.fetchone()

        if( user_flag[0] != 0 ):
            form.errors['username'] = 'Username already exists!'
        else:
            form.data['username'] = username

    email = form['email']
    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """
            SELECT COUNT(USERS.EMAIL)
              FROM USERS
              WHERE USERS.EMAIL = %s
          """
        cursor.execute(query, [email])
        email_flag = cursor.fetchone()

        if (email_flag[0] != 0):
            form.errors['email'] = 'Email already exists!'
        else:
            form.data['email'] = email

    return len(form.errors) == 0

