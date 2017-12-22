Parts Implemented by Hakan Sander
=================================

For the USERNAME and EMAIL validations, following code snippet is used in the program.

The code first checks the emptiness of the required fields. If the fields are empty, the function gives an error message and returns.

If the fields are not empty, the program checks the database and counts the users that has the same username with the entered username.

User Login and Signup Operations
--------------------------------

.. code-block:: python

    def sign_up_validation(form):
        form.data = {}
        form.errors = {}

        if len(form['email'].strip()) == 0:
            form.errors['email'] = 'Email can not be left blank!'
        else:
            form.data['email'] = form['email']

        if len(form['username'].strip()) == 0:
            form.errors['username'] = 'Username can not be left blank!'
        else:
            form.data['username'] = form['username']

        username = form['username']
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """
            SELECT COUNT(USERS.USERNAME)
              FROM USERS
              WHERE USERS.USERNAME = %s
          """
            cursor.execute(query, [username])
            user_flag = cursor.fetchone()

            if( user_flag[0] != 0 ):
                form.errors['username'] = 'Username already exists!'
            else:
                form.data['username'] = username

        email = form['email']
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """
                SELECT COUNT(USERS.EMAIL)
                  FROM USERS
                  WHERE USERS.EMAIL = %s
              """
            cursor.execute(query, [email])
            email_flag = cursor.fetchone()

            if (email_flag[0] != 0):
                form.errors['email'] = 'Email already exists!'
            else:
                form.data['email'] = email

        return len(form.errors) == 0

For the login session, following code snippets are used.

.. code-block:: python

    login_manager = LoginManager()

    @login_manager.user_loader
    def load_user( username ):
      return get_user(username)


For preventing the unauthorized access, following code snippet is used.

.. code-block:: python

    if not current_user.get_is_admin(): #if the user is not admin, then give an error message if the user tries to access admin pages
        abort(401)


.. code-block:: python

    def get_user(db_username):
      with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        statement = """SELECT * FROM USERS WHERE USERNAME = %s"""
        cursor.execute(statement, [db_username])
        db_user = cursor.fetchall()
        user = User(db_user[0][1], db_user[0][2], db_user[0][3],db_user[0][4], db_user[0][5], db_user[0][6])

      if user is not None:
        user.is_admin = user.username in current_app.config['ADMIN_USERS']
      return user


The program checks the config file to control whether a user is admin or not.

The admin is added to the config file with his hashed password in the following way.

.. code-block:: python

    PASSWORDS = {
      'admin': '$6$rounds=656000$NhjGHwap0iYnsrNW$Y0sK0vHaShrBy0Q62GN3TIMQFdcDV7u98tjntyJUfN4EzDGKCr28UaG838uHaRNVCATFomj.d6gc.a1107lZm1'
    }

    ADMIN_USERS = ['admin']


The program checks the ADMIN_USERS and then his password in the PASSWORDS.

For the password hashing, following code is used.

.. code-block:: python

    hashed_password = pwd_context.encrypt(password)


For the password verification, and logging in the user following code is used.

For the user operations, following user class is defined and used.

.. code-block:: python

    class User( UserMixin ):
      def __init__(self, username, password, email, name, surname, faculty_id):
        self.username = username
        self.password = password
        self.email = email
        self.name = name
        self.surname = surname
        self.faculty_id = faculty_id
        self.active = True
        self.is_admin = False

      def get_id(self):
        return self.username
      def get_username(self):
        return self.username
      def get_password(self):
        return self.password
      def get_email(self):
        return self.email
      def get_name(self):
        return self.name
      def get_surname(self):
        return self.surname
      def get_faculty_id(self):
        return self.faculty_id
      def get_is_admin(self):
        return self.is_admin

      @property
      def is_active(self):
        return self.active

      def get_user_id(self, username):
        with dbapi2.connect(current_app.config['dsn']) as connection:
          cursor = connection.cursor()
          statement = """SELECT USERS.ID FROM USERS WHERE USERNAME = %s"""
          cursor.execute(statement, [username])
          db_user_id = cursor.fetchone()
          return db_user_id[0]

      def delete_user_byId(userId):
        if not current_user.is_admin:
          logout_user()

        with dbapi2.connect(current_app.config['dsn']) as connection:
          cursor = connection.cursor()
          statement = """DELETE FROM USERS WHERE USERS.ID = %s"""
          cursor.execute(statement, [userId])


    def get_user(db_username):
      with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        statement = """SELECT * FROM USERS WHERE USERNAME = %s"""
        cursor.execute(statement, [db_username])
        db_user = cursor.fetchall()
        user = User(db_user[0][1], db_user[0][2], db_user[0][3],db_user[0][4], db_user[0][5], db_user[0][6])

      if user is not None:
        user.is_admin = user.username in current_app.config['ADMIN_USERS']
      return user

.. code-block:: python

        if pwd_context.verify(login_password,user.password) is True:
          login_user(user)
          flash('You have succesfully logged in ' + user.get_name() + ' ' + user.get_surname() )
          return redirect((url_for('site.HomePage')))

Restaurants page
----------------

For the restaurant operations, following restaurant class is created.

.. code-block:: python

    class Restaurant:
        def __init__(self, restaurantName, locationID, menuType, restaurantPoint, openingTime, closingTime, ownerEmail, ownerPhone, serviceType):
            self.restaurantName = restaurantName
            self.locationID = locationID
            self.menuType = menuType
            self.restaurantPoint = restaurantPoint
            self.openingTime = openingTime
            self.closingTime = closingTime
            self.ownerEmail = ownerEmail
            self.ownerPhone = ownerPhone
            self.serviceType = serviceType

        def get_restaurant_name(self):
            return self.restaurantName
        def get_location_id(self):
            return self.locationID
        def get_menu_type(self):
            return self.menuType
        def get_restaurant_point(self):
            return self.restaurantPoint
        def get_opening_time(self):
            return self.openingTime
        def get_closing_time(self):
            return self.closingTime
        def get_owner_email(self):
            return self.ownerEmail
        def get_owner_phone(self):
            return self.ownerPhone
        def get_service_type(self):
            return self.serviceType
        def get_id(self):
            return self.id

        def get_restaurant_byId(restaurantId):
            with dbapi2.connect(current_app.config['dsn']) as connection:
                cursor = connection.cursor()
                statement = """SELECT * FROM RESTAURANTS WHERE RESTAURANTS.ID = %s"""
                cursor.execute(statement, [restaurantId])
                db_restaurant = cursor.fetchall()
                restaurant = Restaurant(db_restaurant[0][1], db_restaurant[0][2], db_restaurant[0][3], db_restaurant[0][4], db_restaurant[0][5], db_restaurant[0][6], db_restaurant[0][7], db_restaurant[0][8], db_restaurant[0][9])
                restaurant.id = db_restaurant[0][0]
                return restaurant

        def delete_restaurant_byId(restaurantId):
            with dbapi2.connect(current_app.config['dsn']) as connection:
                cursor = connection.cursor()
                statement = """DELETE FROM RESTAURANTS WHERE RESTAURANTS.ID = %s"""
                cursor.execute(statement, [restaurantId])

The users can vote the restaurant by the following query.

.. code-block:: python

     statement = """UPDATE RESTAURANTS
                                      SET RESTAURANTPOINT = ((RESTAURANTPOINT * VOTES + %s) / ( VOTES + 1 ) ),
                                        VOTES = VOTES + 1
                                    WHERE RESTAURANTS.ID = %s"""

Faculties page
--------------

The following Faculy class is used for the operations related with the faculty.

.. code-block:: python

    class Faculty:
        def __init__(self, facultyName, facultyCode):
            self.facultyName = facultyName
            self.facultyCode = facultyCode

        def get_name(self):
            return self.facultyName
        def get_code(self):
            return self.facultyCode
        def get_id(self):
            return self.id

        def get_faculty_byId(facultyId):
            with dbapi2.connect(current_app.config['dsn']) as connection:
                cursor = connection.cursor()
                statement = """SELECT * FROM FACULTIES WHERE FACULTIES.ID = %s"""
                cursor.execute(statement, [facultyId])
                db_found = cursor.fetchall()
                faculty = Faculty(db_found[0][1], db_found[0][2])
                faculty.id = db_found[0][0]
                return faculty

        def delete_faculty_byId(id):
            with dbapi2.connect(current_app.config['dsn']) as connection:
                cursor = connection.cursor()
                statement = """DELETE FROM FACULTIES WHERE ID = %s"""
                cursor.execute(statement, [id])

For updating a faculty, following code snippet is used.

.. code-block:: python

    if formType == "AddFacultyUpdate":
        formID = request.form['faculty-id']
        with dbapi2.connect(current_app.config['dsn']) as connection:
            faculty = Faculty(facultyName, facultyCode)
            cursor = connection.cursor()
            query = """UPDATE FACULTIES SET FACULTYNAME=%s, FACULTYCODE=%s WHERE ID=%s"""
            cursor.execute(query, (faculty.facultyName, faculty.facultyCode, formID))
        connection.commit()

