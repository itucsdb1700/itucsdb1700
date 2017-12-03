from flask import render_template, Blueprint, current_app, session, redirect, request
from flask.helpers import url_for
from flask_login import current_user, login_user, logout_user, login_required, LoginManager

import psycopg2 as dbapi2

from classes.restaurant_class import Restaurant
from server import load_user
from user import User, get_user
from passlib.apps import custom_app_context as pwd_context
from datetime import datetime
import os.path

from classes.lost_stuff_class import lost_stuff

def restaurants_page():
    if request.method == "POST":
        if 'userSearchButton' in request.form:  # if the search button is submitted
            session['search_username'] = request.form['usernameSearch']
            return redirect(url_for('site.SearchUserPage'))
        formtype = request.form['form-name']

        username = current_user.get_username()
        #print(username) #use print to check whether the correct data is retrieved by checking the terminal
        email = current_user.get_email()
        #print(email)
        name = current_user.get_name()
        #print(name)
        surname = current_user.get_surname()
        #print(surname)

        if formtype == "AddRestaurant":
            restaurantName = request.form['RestaurantName']
            menuType = request.form['MenuType']
            campusLocation = request.form['campusLocation']
            campusLocation = int(campusLocation)
            restaurantPoint = request.form['RestaurantPoint']
            restaurantPoint = int(restaurantPoint)
            openingTime = request.form['OpeningTime']
            closingTime = request.form['ClosingTime']
            restaurantOwnerEmail = request.form['RestaurantOwnerEmail']
            restaurantOwnerPhone = request.form['RestaurantOwnerPhone']
            serviceType = request.form['RestaurantServiceType']

            with dbapi2.connect(current_app.config['dsn']) as connection:
                cursor = connection.cursor()  # prevented sql injection
                restaurant = Restaurant(restaurantName ,campusLocation, menuType, restaurantPoint, openingTime, closingTime, restaurantOwnerEmail, restaurantOwnerPhone, serviceType)
                query = """INSERT INTO RESTAURANTS(RESTAURANTNAME, LOCATIONID, MENUTYPE, RESTAURANTPOINT, OPENINGTIME, CLOSINGTIME, OWNEREMAIL, OWNERPHONENUMBER, SERVICETYPE) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                cursor.execute(query, (restaurant.restaurantName, restaurant.locationID, restaurant.menuType, restaurant.restaurantPoint, restaurant.openingTime, restaurant.closingTime, restaurant.ownerEmail, restaurant.ownerPhone, restaurant.serviceType))
                connection.commit()
            return redirect(url_for('site.RestaurantsPage'))
        elif formtype == "RestaurantUpdate":
            with dbapi2.connect(current_app.config['dsn']) as connection:
                cursor = connection.cursor()#prevented sql injection
                statement = """SELECT ID FROM USERS WHERE (USERS.USERNAME = %s) AND (USERS.EMAIL = %s)"""
                cursor.execute(statement, (username, email))
                lostuser_id = cursor.fetchone()
                lostid = request.form['lost-id']

                lostdesc = request.form['LostSomethingDescription']
                if not lostdesc:
                    statement = """SELECT STUFFDESC FROM LOSTSTUFF WHERE LOSTSTUFF.ID = %s"""
                    cursor.execute(statement, lostid)
                    lostdesc = cursor.fetchone()

                lostlocation = request.form['LostSomethingPossibleLocation']
                if not lostlocation:
                    statement = """SELECT POSSIBLELOC FROM LOSTSTUFF WHERE LOSTSTUFF.ID = %s"""
                    cursor.execute(statement, lostid)
                    lostlocation = cursor.fetchone()

                lostdate = request.form['LostSomethingDate']
                if not lostdate:
                    statement = """SELECT POSSIBLEDATE FROM LOSTSTUFF WHERE LOSTSTUFF.ID = %s"""
                    cursor.execute(statement,lostid)
                    lostdate = cursor.fetchone()

                lostname = request.form['LostSomethingOwnerName']
                if not lostname:
                    statement = """SELECT OWNERNAME FROM LOSTSTUFF WHERE LOSTSTUFF.ID = %s"""
                    cursor.execute(statement, lostid)
                    lostname = cursor.fetchone()

                lostmail = request.form['LostSomethingOwnerMail']
                if not lostmail:
                    statement = """SELECT OWNERMAIL FROM LOSTSTUFF WHERE LOSTSTUFF.ID = %s"""
                    cursor.execute(statement, lostid)
                    lostmail = cursor.fetchone()

                lostphone = request.form['LostSomethingOwnerPhone']
                if not lostphone:
                    statement = """SELECT OWNERPHONE FROM LOSTSTUFF WHERE LOSTSTUFF.ID = %s"""
                    cursor.execute(statement, lostid)
                    lostphone = cursor.fetchone()

                statement = """UPDATE LOSTSTUFF SET STUFFDESC=%s, POSSIBLELOC=%s, POSSIBLEDATE=%s, OWNERNAME=%s, OWNERMAIL=%s, OWNERPHONE=%s, USERID=%s WHERE LOSTSTUFF.ID=%s"""
                cursor.execute(statement, (lostdesc, lostlocation, lostdate, lostname, lostmail, lostphone, lostuser_id, lostid))
                connection.commit()
                return redirect(url_for('site.selected_lost_stuff', lostId=lostid))
    else:
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """
                    SELECT RESTAURANTS.LOCATIONID, 
                      RESTAURANTS.MENUTYPE,
                      RESTAURANTS.RESTAURANTPOINT,
                      RESTAURANTS.OPENINGTIME,
                      RESTAURANTS.CLOSINGTIME,
                      RESTAURANTS.OWNEREMAIL,
                      RESTAURANTS.OWNERPHONENUMBER,
                      RESTAURANTS.SERVICETYPE 
                      FROM RESTAURANTS
            """
            cursor.execute(query)
            restaurants = cursor.fetchall()
        return render_template('restaurants.html', restaurants=restaurants)