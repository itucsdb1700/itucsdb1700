from flask import render_template, Blueprint, abort
from flask import current_app
from datetime import datetime

from flask import redirect
from flask.helpers import url_for, flash

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

from classes.Faculty_class import Faculty


def add_faculty():
    if not current_user.get_is_admin(): #if the user is not admin, then give an error message if the user tries to access admin pages
        abort(401)
    if request.method == 'POST':
        facultyName = request.form['InputFacultyName']
        facultyCode = request.form['InputFacultyCode']

        with dbapi2.connect(current_app.config['dsn']) as connection:
            newFaculty = Faculty(facultyName, facultyCode)

            cursor = connection.cursor()
            query = """INSERT INTO FACULTIES(FACULTYNAME, FACULTYCODE) VALUES (%s, %s)"""
            cursor.execute(query, (newFaculty.facultyName, newFaculty.facultyCode))
            connection.commit()

        return render_template("add_faculty.html")

    else:
        return render_template("add_faculty.html")


