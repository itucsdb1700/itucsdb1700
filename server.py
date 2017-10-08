import os
import json
import re

from flask import Flask, render_template
from flask_login import LoginManager #imported for login page

from handlers import site #Blueprint "site" is included for routing
from user import get_user #imported for login page

lm = LoginManager()

@lm.user_loader
def load_user( user_id ):
  return get_user()

def CreateApp():
    app = Flask(__name__)
    app.config.from_object('settings')
    app.register_blueprint(site) #registering blueprint in the app is needed before they can be used

    lm.init_app(app)
    lm.login_view = 'site.login'

    return app


def get_elephantsql_dsn(vcap_services):
    """Returns the data source name for ElephantSQL."""
    parsed = json.loads(vcap_services)
    uri = parsed["elephantsql"][0]["credentials"]["uri"]
    match = re.match('postgres://(.*?):(.*?)@(.*?)(:(\d+))?/(.*)', uri)
    user, password, host, _, port, dbname = match.groups()
    dsn = """user='{}' password='{}' host='{}' port={}
             dbname='{}'""".format(user, password, host, port, dbname)
    return dsn


def main():
    VCAP_APP_PORT = os.getenv('VCAP_APP_PORT')
    # PORT no is changed to 5000 from 8080 since windows gives an error message
    if VCAP_APP_PORT is not None:
      port = int(VCAP_APP_PORT)
      debug = False
    else:
      port = app.config.get('PORT', 5000)
      debug = app.config['DEBUG']


    VCAP_SERVICES = os.getenv('VCAP_SERVICES')
    if VCAP_SERVICES is not None:
        app.config['dsn'] = get_elephantsql_dsn(VCAP_SERVICES)
    else:
        app.config['dsn'] = """user='vagrant' password='vagrant'
                                   host='localhost' port=5432 dbname='itucsdb'"""

    app.run(host='0.0.0.0', port=port, debug=debug)


if __name__ == '__main__':
    app = CreateApp()
    main()



