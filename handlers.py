#this file contains the necessary handler functions
#instead of the app, blueprint is used for routing now

from flask import Blueprint

site = Blueprint('site', __name__)

from handler_operations.lost_stuff import *
from handler_operations.found_stuff import *
from handler_operations.login import *
from handler_operations.sign_up import *
from handler_operations.restaurants import *
from handler_operations.game_friends import *
from handler_operations.initdb import *
from handler_operations.sharedMyHouseAnnouncement import *
from handler_operations.searchedHouseAnnouncement import *
from handler_operations.special_tutor import *
from handler_operations.special_student import *
from handler_operations.itu_activities import *
from handler_operations.club_activities import *
from handler_operations.sport_activities import *
from handler_operations.sharedBooksAnnouncement import *
from handler_operations.sharedLessonNotesAnnouncement import *


@site.route('/count')
@login_required
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

@site.route('/', methods=['GET', 'POST'])
def LoginPage():
    return login_page()

@site.route("/logout")
@login_required
def LogoutPage():
  logout_user()
  return redirect(url_for('site.LoginPage'))

@site.route('/initdb')
def initialize_database():
    LogoutPage()
    return init_db()


@site.route('/home')
@login_required
def HomePage():
    now = datetime.now()
    return render_template('home.html', current_time=now.ctime())


@site.route('/sharemyhouse_announcement',methods=['GET', 'POST'])
@login_required
def ShareMyHousePageAnnouncement():
    return share_MyHouse_Announcement_Page()

@site.route('/searchedhouse_announcement',methods=['GET', 'POST'])
@login_required
def SearchedHousePageAnnouncement():
    return searched_House_Announcement_Page()


@site.route('/sharebooks',methods = ['GET','POST'])
@login_required
def SharedBooksAnnouncementPage():
    return shared_Books_Announcement_Page()

@site.route('/sharelessonnotes',methods = ['GET','POST'])
@login_required
def SharedLessonNotesAnnouncementPage():
    return shared_LessonNotes_Announcement_Page()

@site.route('/sign_up', methods=['GET', 'POST'])
def SignUpPage():
  return sign_up_page()


@site.route('/game_friends', methods=['GET', 'POST'])
@login_required
def GameFriendPage():
    return game_friend_page()


@site.route('/lost_stuff', methods=['GET', 'POST'])
@login_required
def LostStuff():
    return lost_stuff_page()

@site.route('/found_stuff', methods=['GET', 'POST'])
@login_required
def FoundStuff():
    return found_stuff_page()

@site.route('/restaurants', methods=['GET', 'POST'])
@login_required
def RestaurantsPage():
    return restaurants_page()

@site.route('/special_tutors', methods=['GET', 'POST'])
@login_required
def SpecialTutor():
    return special_tutor_page()

@site.route('/special_students', methods=['GET', 'POST'])
@login_required
def SpecialStudent():
    return special_student_page()

@site.route('/club_activities', methods=['GET', 'POST'])
@login_required
def ClubActivityPage():
    return club_activity_page()

@site.route('/sport_activities', methods=['GET', 'POST'])
@login_required
def SportActivityPage():
    return sport_activity_page()

@site.route('/itu_activities', methods=['GET', 'POST'])
@login_required
def ItuActivityPage():
    return itu_activity_page()