from flask import current_app
from flask_login import UserMixin
import psycopg2 as dbapi2
from flask_login import logout_user

class User( UserMixin ):
  def __init__(self, username, password, email, name, surname, faculty_id):
    self.username = username
    self.password = password
    self.email = email
    self.name = name
    self.surname = surname
    self.faculty_id = faculty_id
    self.active = True
    self.is_admin = False

  def get_id(self):
    return self.username
  def get_username(self):
    return self.username
  def get_password(self):
    return self.password
  def get_email(self):
    return self.email
  def get_name(self):
    return self.name
  def get_surname(self):
    return self.surname
  def get_faculty_id(self):
    return self.faculty_id
  def get_is_admin(self):
    return self.is_admin

  @property
  def is_active(self):
    return self.active

  def get_user_id(self, username):
    with dbapi2.connect(current_app.config['dsn']) as connection:
      cursor = connection.cursor()
      statement = """SELECT USERS.ID FROM USERS WHERE USERNAME = %s"""
      cursor.execute(statement, [username])
      db_user_id = cursor.fetchone()
      return db_user_id[0]

  def delete_user_byId(userId):
     logout_user()
     with dbapi2.connect(current_app.config['dsn']) as connection:
          cursor = connection.cursor()
          statement = """DELETE FROM USERS WHERE USERS.ID = %s"""
          cursor.execute(statement, [userId])


def get_user(db_username):
  #password = current_app.config['PASSWORD'].get(user_id)
  with dbapi2.connect(current_app.config['dsn']) as connection:
    cursor = connection.cursor()
    statement = """SELECT * FROM USERS WHERE USERNAME = %s"""
    cursor.execute(statement, [db_username])
    db_user = cursor.fetchall()
    user = User(db_user[0][1], db_user[0][2], db_user[0][3],db_user[0][4], db_user[0][5], db_user[0][6])
    #print('%s' % db_user[0][0])

  if user is not None:
    user.is_admin = user.username in current_app.config['ADMIN_USERS']
  return user