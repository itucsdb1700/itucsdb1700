#this file contains the necessary handler functions
#instead of the app, blueprint is used for routing now

from flask import Blueprint

site = Blueprint('site', __name__)

from handler_operations.lost_found import *
from handler_operations.house_announcement import *
from handler_operations.login import *
from handler_operations.sign_up import *
from handler_operations.restaurants import *
from handler_operations.game_friends import *
from handler_operations.initdb import *

@site.route('/count')
def counter_page():
    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = "UPDATE COUNTER SET N = N + 1"
        cursor.execute(query)
        connection.commit()

        query = "SELECT N FROM COUNTER"
        cursor.execute(query)
        count = cursor.fetchone()[0]
    return "This page was accessed %d times." % count


#@login_required
@site.route('/initdb')
def initialize_database():
    return init_db()


@site.route('/home')
def HomePage():
    now = datetime.now()
    return render_template('home.html', current_time=now.ctime())


@site.route('/house_announcement',  methods=['GET', 'POST'])
@login_required
def HousePage():
    return house_announcement_page()

@site.route('/', methods=['GET', 'POST'])
def LoginPage():
    return login_page()

@site.route('/sign_up', methods=['GET', 'POST'])
def SignUpPage():
  return sign_up_page()


@site.route('/game_friends', methods=['GET', 'POST'])
def GameFriendPage():
    return game_friend_page()


@site.route('/lost_found', methods=['GET', 'POST'])
def PropertyPage():
    return lost_found_page()

@site.route('/restaurants', methods=['GET', 'POST'])
def RestaurantsPage():
    return restaurants_page()

@site.route("/logout")
@login_required
def LogoutPage():
  logout_user()
  return redirect(url_for('LoginPage'))