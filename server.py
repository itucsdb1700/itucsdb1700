import datetime
import os

from flask import Flask, render_template
from handlers import site #Blueprint "site" is included for routing

def CreateApp():
    app = Flask(__name__)
    app.config.from_object('settings')
    app.register_blueprint(site) #registering blueprint in the app is needed before they can be used
    return app


def main():
    app = CreateApp()
    debug = app.config['DEBUG']
    port = app.config.get('PORT', 5000)
    app.run(host='0.0.0.0', port=port, debug=debug) #PORT no is changed to 5000 from 8080 since windows gives an error message

if __name__ == '__main__':
    main()






##We may need the code below

#if __name__ == '__main__':
#   VCAP_APP_PORT = os.getenv('VCAP_APP_PORT')
#    if VCAP_APP_PORT is not None:
#        port, debug = int(VCAP_APP_PORT), False
#    else:
#        port, debug = 5000, True
#    app.run(host='0.0.0.0', port=port, debug=debug)
