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

#under development...
def search_user_page(username):
  if request.method == "POST":
    search_username = request.form['usernameSearch']
    if search_username:
      with dbapi2.connect(current_app.config['dsn']) as connection:
        edited_search_username = search_username + '%'
        print(edited_search_username)
        cursor = connection.cursor()
        query = """SELECT USERS.USERNAME, USERS.NAME, USERS.SURNAME, USERS.EMAIL
                    FROM  USERS
                    WHERE ( USERS.USERNAME LIKE %s )"""
        cursor.execute(query, [edited_search_username])
        found_user = cursor.fetchall()
        print('%s' % found_user[1][1])
        return render_template('search_users.html', found_user=found_user)
  else:
    return render_template('restaurants.html')