from flask import current_app
from flask_login import UserMixin
import psycopg2 as dbapi2

class User( UserMixin ):
  def __init__(self, username, password, email):
    self.username = username
    self.password = password
    self.email = email
    self.active = True
    self.is_admin = False

  def get_id(self):
    return self.username

  @property
  def is_active(self):
    return self.active

def get_user(db_username):
  #password = current_app.config['PASSWORD'].get(user_id)
  with dbapi2.connect(current_app.config['dsn']) as connection:
    cursor = connection.cursor()
    statement = """SELECT * FROM USERS WHERE USERNAME = %s"""
    cursor.execute(statement, [db_username])
    db_user = cursor.fetchall()
    user = User(db_user[0][1], db_user[0][2], db_user[0][3])
    print('%s' % db_user[0][0])

  if user is not None:
    user.is_admin = user.username in current_app.config['ADMIN_USERS']
  return user