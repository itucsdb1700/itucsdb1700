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
from handler_operations.sharedHouseAnnouncement import *
from handler_operations.searchedHouseAnnouncement import *
from handler_operations.special_tutor import *
from handler_operations.special_student import *
from handler_operations.itu_activities import *
from handler_operations.club_activities import *
from handler_operations.sport_activities import *
from handler_operations.sharedBooksAnnouncement import *
from handler_operations.sharedLessonNotesAnnouncement import *
from handler_operations.searchedHouseAnnouncementForProfile import *
from handler_operations.sharedHouseAnnouncementForProfile import *
from handler_operations.sharedBooksAnnouncementForProfile import *
from handler_operations.sharedLessonNotesAnnouncementForProfile import *
from handler_operations.add_faculty import *
from handler_operations.search_user import *
from handler_operations.list_users import *
from handler_operations.home import *


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

@site.route('/sign_up', methods=['GET', 'POST'])
def SignUpPage():
  return sign_up_page()

@site.route("/logout")
@login_required
def LogoutPage():
  logout_user()
  return redirect(url_for('site.LoginPage'))

@site.route('/initdb')
@login_required
def initialize_database():
    LogoutPage()
    return init_db()

@site.route('/add_faculty', methods=['GET', 'POST'])
@login_required
def AddFaculty():
    return add_faculty()

@site.route('/home', methods=['GET', 'POST'])
@login_required
def HomePage():
    now = datetime.now()
    return home_page()

@site.route('/profile')
@login_required
def ProfilePage():
    return redirect(url_for('site.SelectedProfilePage', username=current_user.get_username()))

@site.route('/profile/<string:username>', methods=['GET', 'POST'])
@login_required
def SelectedProfilePage(username):
    if request.method == 'POST':
        if 'userSearchButton' in request.form:  # if the search button is submitted
            session['search_username'] = request.form['usernameSearch']
            return redirect(url_for('site.SearchUserPage'))

    if CheckUser(username): #returns 0 if the username does not exist
        user = get_user(username) #create the user object
        return render_template('profile.html', user=user) #send the user object to the html
    else:
        return redirect(url_for('site.HomePage'))

@site.route('/search_user', methods=['GET', 'POST'])
@login_required
def SearchUserPage():
    return search_user_page()

@site.route('/list_user', methods=['GET', 'POST'])
@login_required
def ListUsers():
    return list_users_page()

def CheckUser(username):
    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        statement = """SELECT COUNT(USERS.USERNAME) 
                        FROM USERS 
                        WHERE (USERS.USERNAME = %s)"""
        cursor.execute(statement, [username])
        existence_flag = cursor.fetchone()
        return existence_flag[0]

######################################################################

@site.route('/sharemyhouse_announcement',methods=['GET', 'POST'])
@login_required
def ShareHousePageAnnouncement():
    return share_MyHouse_Announcement_Page()

@site.route('/my_shared_house_announcement',methods = ['GET','POST'])
@login_required
def ProfileOfSharingHouseAnnouncementPage():
    return shared_House_Announcement_For_Profile_Page();

@site.route('/delete_shared_house_announcement/<int:id>',methods = ['POST'])
@login_required
def deleteSharedHouse(id):
    sharingHouseAnnouncement.delete_sharingHouseAnnouncement_byId(id)
    return redirect(url_for('site.ProfileOfSharingHouseAnnouncementPage'))

##################################################
@site.route('/sharebooks',methods = ['GET','POST'])
@login_required
def SharedBooksAnnouncementPage():
    return shared_Books_Announcement_Page()

@site.route('/my_shared_books_announcement',methods = ['GET','POST'])
@login_required
def ProfileOfSharingBooksAnnouncementPage():
    return shared_Books_Announcement_For_Profile_Page();

@site.route('/delete_shared_books_announcement/<int:id>',methods = ['POST'])
@login_required
def deleteSharedBooks(id):
    sharingBooksAnnouncement.delete_sharingBooksAnnouncement_byId(id)
    return redirect(url_for('site.ProfileOfBooksAnnouncementPage'))
#################################################


@site.route('/sharelessonnotes',methods = ['GET','POST'])
@login_required
def SharedLessonNotesAnnouncementPage():
    return shared_LessonNotes_Announcement_Page()

@site.route('/my_shared_lessonnotes_announcement',methods = ['GET','POST'])
@login_required
def ProfileOfSharingLessonNotesAnnouncementPage():
    return shared_LessonNotes_Announcement_For_Profile_Page();

@site.route('/delete_shared_lessonnotes_announcement/<int:id>',methods = ['POST'])
@login_required
def deleteSharedLessonNotes(id):
    sharingLessonNotesAnnouncement.delete_sharingLessonNotesAnnouncement_byId(id)
    return redirect(url_for('site.ProfileOfLessonNotesHouseAnnouncementPage'))

#######################################################################
@site.route('/searchedhouse_announcement',methods=['GET', 'POST'])
@login_required
def SearchedHousePageAnnouncement():
    return searched_House_Announcement_Page()

@site.route('/my_searched_house_announcement',methods = ['GET','POST'])
@login_required
def ProfileOfSearchingHouseAnnouncementPage():
    return searched_House_Announcement_For_Profile_Page();

@site.route('/delete_searched_house_announcement/<int:id>',methods = ['POST'])
@login_required
def deleteSearchedHouse(id):
    searchingHouseAnnouncement.delete_searchingHouseAnnouncement_byId(id)
    return redirect(url_for('site.ProfileOfSearchingHouseAnnouncementPage'))
#######################################################################


@site.route('/lost_stuff', methods=['GET', 'POST'])
@login_required
def LostStuff():
    return lost_stuff_page()

@site.route('/lost_stuff/<string:lostId>')
@login_required
def selected_lost_stuff(lostId):
    lost = lost_stuff.get_lost_byId(lostId)
    lost_user_id = lost.get_user_id()
    #print(lost_user_id)
    email = current_user.get_email()
    username = current_user.get_username()
    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()  # prevented sql injection
        statement = """SELECT ID FROM USERS WHERE (USERS.USERNAME = %s) AND (USERS.EMAIL = %s)"""
        cursor.execute(statement, (username, email))
        user_id = cursor.fetchone()
        #print(int(user_id[0]))
        return render_template('lost_stuff_details.html', lost = lost, lost_user_id=lost_user_id, user_id = int(user_id[0]))

@site.route('/delete_lost_stuff/<int:id>', methods=['POST'])
def delete_lost_stuff(id):
    lost_stuff.delete_lost_byId(id)
    return redirect(url_for('site.LostStuff'))

@site.route('/found_stuff', methods=['GET', 'POST'])
@login_required
def FoundStuff():
    return found_stuff_page()

@site.route('/found_stuff/<string:foundId>')
@login_required
def selected_found_stuff(foundId):
    found = found_stuff.get_found_byId(foundId)
    found_user_id = found.get_user_id()
    email = current_user.get_email()
    username = current_user.get_username()
    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()  # prevented sql injection
        statement = """SELECT ID FROM USERS WHERE (USERS.USERNAME = %s) AND (USERS.EMAIL = %s)"""
        cursor.execute(statement, (username, email))
        user_id = cursor.fetchone()
        return render_template('found_stuff_details.html', found=found, found_user_id=found_user_id, user_id=int(user_id[0]))

@site.route('/delete_found_stuff/<int:id>', methods=['POST'])
def delete_found_stuff(id):
    found_stuff.delete_found_byId(id)
    return redirect(url_for('site.FoundStuff'))

@site.route('/restaurants', methods=['GET', 'POST'])
@login_required
def RestaurantsPage():
    return restaurants_page()

@site.route('/special_tutors', methods=['GET', 'POST'])
@login_required
def SpecialTutor():
    return special_tutor_page()

@site.route('/special_tutors/<string:tutorId>')
@login_required
def selected_special_tutor(tutorId):
    tutor = special_tutor.get_tutor_byId(tutorId)
    return render_template('special_tutor_details.html', tutor=tutor)

@site.route('/delete_special_tutor/<int:id>', methods=['POST'])
def delete_special_tutor(id):
    special_tutor.delete_tutor_byId(id)
    return redirect(url_for('site.SpecialTutor'))

@site.route('/special_students', methods=['GET', 'POST'])
@login_required
def SpecialStudent():
    return special_student_page()

@site.route('/special_students/<string:studentId>')
@login_required
def selected_special_student(studentId):
    student = special_student.get_student_byId(studentId)
    return render_template('special_student_details.html', student=student)

@site.route('/delete_special_student/<int:id>', methods=['POST'])
def delete_special_student(id):
    special_student.delete_student_byId(id)
    return redirect(url_for('site.SpecialStudent'))


#######################################################################


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

@site.route('/game_friends', methods=['GET', 'POST'])
@login_required
def GameFriendPage():
    return game_friend_page()


@site.route('/game_friends/<string:announceId>')
@login_required
def SelectedGameAnnounce(announceId):
    announce = GameAnnounce.get_announce_byId(announceId)
    return render_template('game_friend_announces.html', announce=announce)

@site.route('/delete_game_friends/<int:id>', methods=['POST'])
@login_required
def deleteGameFriend(id):
    GameAnnounce.delete_announce_byId(id)
    return redirect(url_for('site.GameFriendPage'))


@site.route('/itu_activities/<string:activityId>')
@login_required
def SelectedItuActivity(activityId):
    activity = ItuActivity.get_activity_byId(activityId)
    return render_template('itu_activities_detail.html', activity=activity)

@site.route('/delete_itu_activity/<int:id>', methods=['POST'])
@login_required
def DeleteItuActivity(id):
    ItuActivity.delete_activity_byId(id)
    return redirect(url_for('site.ItuActivityPage'))


@site.route('/club_activities/<string:activityId>')
@login_required
def SelectedClubActivity(activityId):
    activity = ClubActivity.get_activity_byId(activityId)
    return render_template('club_activities_detail.html', activity=activity)

@site.route('/delete_club_activity/<int:id>', methods=['POST'])
@login_required
def DeleteClubActivity(id):
    ClubActivity.delete_activity_byId(id)
    return redirect(url_for('site.ClubActivityPage'))


@site.route('/sport_activities/<string:activityId>')
@login_required
def SelectedSportActivity(activityId):
    activity = SportActivity.get_activity_byId(activityId)
    return render_template('sport_activities_detail.html', activity=activity)

@site.route('/delete_sport_activity/<int:id>', methods=['POST'])
@login_required
def DeleteSportActivity(id):
    SportActivity.delete_activity_byId(id)
    return redirect(url_for('site.SportActivityPage'))
