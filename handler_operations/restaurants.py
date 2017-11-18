from flask import render_template, Blueprint
from flask import current_app
from datetime import datetime
from flask import session

from flask import redirect
from flask.helpers import url_for

from flask_login import login_required
from flask_login import current_user, login_user, logout_user

from handler_operations.search_user import search_user_page
from user import User
from user import get_user
from flask_login import LoginManager
from flask import request

from passlib.apps import custom_app_context as pwd_context

import psycopg2 as dbapi2
import os.path

from server import load_user

#under development...
def restaurants_page():
  if request.method == "POST":

    session['search_username'] = request.form['usernameSearch']
    if session['search_username']:
      return redirect(url_for('site.SearchUserPage'))
    else:
      return render_template('restaurants.html')
  else:
    return render_template('restaurants.html')