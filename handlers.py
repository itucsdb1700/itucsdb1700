#this file contains the necessary handler functions
#instead of the app, blueprint is used for routing now

from flask import render_template, Blueprint
from datetime import datetime

site = Blueprint('site', __name__)

@site.route('/')
def HomePage():
    now = datetime.now()
    return render_template('home.html', current_time=now.ctime())

@site.route('/house_announcement')
def HousePage():
    return render_template('house_announcement.html')   

@site.route('/lost_properties')
def PropertyPage():
    return render_template('lost_properties.html')