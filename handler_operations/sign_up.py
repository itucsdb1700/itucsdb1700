from flask import render_template
from flask import current_app
from flask import redirect
from flask import request
from flask.helpers import url_for
from passlib.apps import custom_app_context as pwd_context
import psycopg2 as dbapi2
from handler_operations.sign_up_validation import *


def sign_up_page():
  if request.method == 'POST':
    valid = sign_up_validation(request.form)

    if valid:
      username = request.form['username']
      email = request.form['email']
      password = request.form['password']
      hashed_password = pwd_context.encrypt(password)
      name = request.form['firstName']
      surname = request.form['lastName']
      faculty = request.form['faculty']

      with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """SELECT FACULTIES.ID
                    FROM FACULTIES 
                    WHERE FACULTIES.FACULTYNAME = %s
          """
        cursor.execute(query, [faculty])
        faculty_id = cursor.fetchone()

      with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """
                INSERT INTO USERS (USERNAME, PASSWORD, EMAIL, NAME, SURNAME, FACULTYID) 
                  VALUES (%s, %s, %s, %s, %s, %s)"""

        cursor.execute(query, (username, hashed_password, email, name, surname, faculty_id))

        connection.commit()
      return redirect(url_for('site.LoginPage'))
    else:
      with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """SELECT FACULTIES.FACULTYNAME, FACULTIES.FACULTYCODE 
                    FROM FACULTIES 
                    """
        cursor.execute(query)
        allFaculties = cursor.fetchall()

      form = request.form
      return render_template('sign_up.html', form=form, allFaculties=allFaculties)




  else: #else the method is GET
    with dbapi2.connect(current_app.config['dsn']) as connection:
      cursor = connection.cursor()
      query = """SELECT FACULTIES.FACULTYNAME, FACULTIES.FACULTYCODE 
                  FROM FACULTIES 
                  """
      cursor.execute(query)
      allFaculties = cursor.fetchall()
    return render_template('sign_up.html', allFaculties=allFaculties)