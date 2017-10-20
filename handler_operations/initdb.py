from flask import current_app
from flask import redirect
from flask.helpers import url_for

import psycopg2 as dbapi2

def init_db():
    with dbapi2.connect(current_app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            with current_app.open_resource('script.sql', 'r') as file:
                statements = file.read()
                cursor.execute(statements)

    return redirect(url_for('site.HomePage'))
