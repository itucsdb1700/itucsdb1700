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
import handlers

from passlib.apps import custom_app_context as pwd_context

import psycopg2 as dbapi2
import os.path

from server import load_user

def login_page():
  if request.method == 'POST':
    login_email = request.form['login_email']
    print( "%s" % login_email)
    login_password = request.form['login_password']

    with dbapi2.connect(current_app.config['dsn']) as connection:
      cursor = connection.cursor()
      statement = """SELECT USERNAME FROM USERS WHERE USERNAME = %s"""
      cursor.execute(statement, [login_email])
      db_username = cursor.fetchone()

      if db_username is not None:  # check whether the user exists
        user = load_user(db_username)
        statement = """SELECT PASSWORD FROM USERS WHERE USERNAME = %s"""
        cursor.execute(statement, [login_email])
        if pwd_context.verify(login_password,user.password) is True:
          login_user(user)
          return redirect((url_for('site.HomePage')))
        else:
          return render_template('login.html')
      else:
        return render_template('login.html')
        # print('%s %s' % db_username[0][0], db_username[0][1] ) if the fetchall method is used debug using this line
  else:
    return render_template('login.html')