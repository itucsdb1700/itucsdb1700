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

def sign_up_page():
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
            VALUES (%s, %s, %s)"""

      cursor.execute(query, (username, hashed_password, email))

      connection.commit()
    return redirect(url_for('site.LoginPage'))

  else:
    return render_template('sign_up.html')