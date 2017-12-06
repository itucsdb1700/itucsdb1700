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

            with dbapi2.connect(current_app.config['dsn']) as connection: #get the id of the selected campusLocation from the dropdown list
                cursor = connection.cursor()
                query = """SELECT CAMPUSLOCATIONS.ID
                          FROM CAMPUSLOCATIONS
                          WHERE CAMPUSLOCATIONS.CAMPUSNAME= %s
                """
                cursor.execute(query, [campusLocation])
                campusLocation = cursor.fetchone()

            restaurantPoint = request.form['RestaurantPoint']
            restaurantPoint = int(restaurantPoint)
            openingTime = request.form['OpeningTime']
            closingTime = request.form['ClosingTime']
            restaurantOwnerEmail = request.form['RestaurantOwnerEmail']
            restaurantOwnerPhone = request.form['RestaurantOwnerPhone']
            serviceType = request.form['RestaurantServiceType']

            with dbapi2.connect(current_app.config['dsn']) as connection:
                cursor = connection.cursor()  # prevented sql injection
                restaurant = Restaurant(restaurantName ,campusLocation[0], menuType, restaurantPoint, openingTime, closingTime, restaurantOwnerEmail, restaurantOwnerPhone, serviceType)
                query = """INSERT INTO RESTAURANTS(RESTAURANTNAME, LOCATIONID, MENUTYPE, RESTAURANTPOINT, OPENINGTIME, CLOSINGTIME, OWNEREMAIL, OWNERPHONENUMBER, SERVICETYPE) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                cursor.execute(query, (restaurant.restaurantName, restaurant.locationID, restaurant.menuType, restaurant.restaurantPoint, restaurant.openingTime, restaurant.closingTime, restaurant.ownerEmail, restaurant.ownerPhone, restaurant.serviceType))
                connection.commit()
            return redirect(url_for('site.RestaurantsPage'))

        elif formtype == "RestaurantUpdate":
            with dbapi2.connect(current_app.config['dsn']) as connection:
                cursor = connection.cursor()
                restaurantId = request.form['restaurant-id']

                restaurantName = request.form['RestaurantName']
                if not restaurantName:
                    statement = """SELECT RESTAURANTNAME FROM RESTAURANTS WHERE RESTAURANTS.ID = %s"""
                    cursor.execute(statement, restaurantId)
                    restaurantName = cursor.fetchone()

                menuType = request.form['MenuType']
                if not menuType:
                    statement = """SELECT MENUTYPE FROM RESTAURANTS WHERE RESTAURANTS.ID = %s"""
                    cursor.execute(statement, restaurantId)
                    menuType= cursor.fetchone()

                campusLocation = request.form['campusLocation']
                if not campusLocation:
                    statement = """SELECT LOCATIONID FROM RESTAURANTS WHERE RESTAURANTS.ID = %s"""
                    cursor.execute(statement, restaurantId)
                    campusLocation = cursor.fetchone()

                else: #get the location id
                    statement = """SELECT CAMPUSLOCATIONS.ID FROM CAMPUSLOCATIONS WHERE CAMPUSLOCATIONS.CAMPUSNAME = %s"""
                    cursor.execute(statement, [campusLocation])
                    campusLocation = cursor.fetchone()
                restaurantPoint = request.form['RestaurantPoint']
                if not restaurantPoint:
                    statement = """SELECT RESTAURANTPOINT FROM RESTAURANTS WHERE RESTAURANTS.ID = %s"""
                    cursor.execute(statement, restaurantId)
                    restaurantPoint = cursor.fetchone()

                restaurantOwnerEmail = request.form['RestaurantOwnerEmail']
                if not restaurantOwnerEmail:
                    statement = """SELECT OWNEREMAIL FROM RESTAURANTS WHERE RESTAURANTS.ID = %s"""
                    cursor.execute(statement, restaurantId)
                    restaurantOwnerEmail = cursor.fetchone()

                restaurantOwnerPhone = request.form['RestaurantOwnerPhone']
                if not restaurantOwnerPhone:
                    statement = """SELECT OWNERPHONENUMBER FROM RESTAURANTS WHERE RESTAURANTS.ID = %s"""
                    cursor.execute(statement, restaurantId)
                    restaurantOwnerPhone = cursor.fetchone()

                openingTime = request.form['OpeningTime']
                if not openingTime:
                    statement = """SELECT OPENINGTIME FROM RESTAURANTS WHERE RESTAURANTS.ID = %s"""
                    cursor.execute(statement, restaurantId)
                    openingTime = cursor.fetchone()


                closingTime = request.form['ClosingTime']
                if not closingTime:
                    statement = """SELECT CLOSINGTIME FROM RESTAURANTS WHERE RESTAURANTS.ID = %s"""
                    cursor.execute(statement, restaurantId)
                    closingTime = cursor.fetchone()

                serviceType = request.form['RestaurantServiceType']
                if not serviceType:
                    statement = """SELECT SERVICETYPE FROM RESTAURANTS WHERE RESTAURANTS.ID = %s"""
                    cursor.execute(statement, restaurantId)
                    serviceType = cursor.fetchone()

                statement = """UPDATE RESTAURANTS SET RESTAURANTNAME = %s, LOCATIONID= %s, MENUTYPE= %s, RESTAURANTPOINT = %s, OPENINGTIME = %s, CLOSINGTIME = %s,
                                OWNEREMAIL = %s, OWNERPHONENUMBER = %s, SERVICETYPE = %s WHERE RESTAURANTS.ID = %s"""
                cursor.execute(statement,
                               (restaurantName, campusLocation[0], menuType, restaurantPoint, openingTime, closingTime, restaurantOwnerEmail, restaurantOwnerPhone, serviceType, restaurantId))
                connection.commit()

                return redirect(url_for('site.SelectedRestaurant', restaurantId=restaurantId))

        elif formtype == "VoteUpdate":
            restaurantId = request.form['restaurant-id']
            newPoint = request.form['point']
            print(newPoint)
            return redirect(url_for('site.SelectedRestaurant', restaurantId=restaurantId))



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
                      RESTAURANTS.SERVICETYPE, 
                      RESTAURANTS.ID
                      FROM RESTAURANTS
            """
            cursor.execute(query)
            restaurants = cursor.fetchall()

        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """SELECT CAMPUSLOCATIONS.CAMPUSDISTRICT, CAMPUSLOCATIONS.CAMPUSNAME
                         FROM CAMPUSLOCATIONS 
                        """
            cursor.execute(query)
            campusLocations = cursor.fetchall()

        pointList = [1,2,3,4,5]
        return render_template('restaurants.html', restaurants=restaurants, campusLocations=campusLocations, pointList=pointList)