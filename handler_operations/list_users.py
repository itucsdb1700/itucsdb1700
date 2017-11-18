from flask import render_template, Blueprint
from flask import current_app
from datetime import datetime
from flask import session
from flask import redirect
from flask.helpers import url_for
from handlers import *

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
def list_users_page():
    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """SELECT USERS.ID, USERS.USERNAME, USERS.NAME, USERS.SURNAME, USERS.EMAIL, USERS.FACULTYID FROM USERS """
        cursor.execute(query)
        user_list = cursor.fetchall()
        return render_template('list_users.html', user_list=user_list)