Parts Implemented by Sercan Şahan
=================================

Pages and tables that are related to them are explained below:

Special Tutors page is related to SPECIALTUTORS table.

Special Students page is related to SPECIALSTUDENTS table.

Lost Stuff page is related to LOSTSTUFF table.

Found Stuff page is related to FOUNDSTUFF table.

.. raw:: latex

    \newpage

Special Tutors Page
-------------------

This page uses a class structure to manage inputs from users. It structure is shown below. It is placed at classes/special_tutor_class.py file.

.. code-block:: python

      class special_tutor:
            def __init__(self, subject, fullname, email, phonenumber, user_id):
                  self.subject = subject
                  self.fullname = fullname
                  self.email = email
                  self.phonenumber = phonenumber
                  self.user_id = user_id

This class have different methods to manipulate data.

One of these methods is used to get data of entry by using ID. This method returns an object with type of special_tutor by getting information from database.

.. code-block:: python

      def get_tutor_byId(tutorId):
            with dbapi2.connect(current_app.config['dsn']) as connection:
                  cursor = connection.cursor()
                  statement = """SELECT * FROM SPECIALTUTORS WHERE SPECIALTUTORS.ID = %s"""
                  cursor.execute(statement, [tutorId])
                  db_tutor = cursor.fetchall()
                  tutor = special_tutor(db_tutor[0][1], db_tutor[0][2], db_tutor[0][3], db_tutor[0][4], db_tutor[0][5])
                  tutor.id = db_tutor[0][0]
            return tutor

Another method is used to delete entries from database. This method get ID of entry and deletes it from database table.

.. code-block:: python

      def delete_tutor_byId(tutorId):
            with dbapi2.connect(current_app.config['dsn']) as connection:
                  cursor = connection.cursor()
                  statement = """DELETE FROM SPECIALTUTORS WHERE SPECIALTUTORS.ID = %s"""
                  cursor.execute(statement, [tutorId])

At the beginning of special_tutor.py file, action's type decides next operations. If method is POST, it means user submitted a form. If method is GET, it means user is only displaying the page.

.. code-block:: python

      if request.method == "POST":

After that, if method is POST it is checked that if search box in top bar is used. If that search box is used, user is redirected to result page of their search.

.. code-block:: python

      if 'userSearchButton' in request.form: #if the search button is submitted
            session['search_username'] = request.form['usernameSearch']
            return redirect(url_for('site.SearchUserPage'))

If user did not use the search box, submitted form's type is taken via a hidden input to check form's purpose.

.. code-block:: python

      formtype = request.form['form-name']

After getting form type, information of current user is taken for later user.

.. code-block:: python

      username = current_user.get_username()
      email = current_user.get_email()
      name = current_user.get_name()
      surname = current_user.get_surname()

The code below is executed if user submits the form that creates new entry. At the beginning, data in the form is taken via request.form action. However, user have an option to leave name and mail blank. If they leave it blank, current user's information that taken before is used.

After that, psycopg2's database connection is used. A cursor that will be used for this database connection is created and SQL command is assigned to a statement. This statement pulls current user's ID from database and assigns it to a variable for later usage.

After getting all required information, an object is created for easier usage. A SQL statement is created and assigned to query variable. With database connection, query and object's data is submitted and a new row in database table is created.

After finishing work with database connection, it is closed. After all work is done, user is redirected to Special Tutor page to prevent submitting form for a second time by using refresh.

.. code-block:: python

      if formtype == "SpecialTutor":
            tutorsubject = request.form['SpecialTutorSubject']
            tutorname = request.form['SpecialTutorName']
            if not tutorname:
                seq = {name, surname}
                tutorname = " ".join(seq)
            tutormail = request.form['SpecialTutorMail']
            if not tutormail:
                tutormail = email
            tutorphone = request.form['SpecialTutorPhone']
            with dbapi2.connect(current_app.config['dsn']) as connection:
                cursor = connection.cursor()
                statement = """SELECT ID FROM USERS WHERE (USERS.USERNAME = %s) AND (USERS.EMAIL = %s)"""
                cursor.execute(statement, (username, email))
                tutorid = cursor.fetchone()
                tutor = special_tutor(tutorsubject, tutorname, tutormail, tutorphone, tutorid)
                query = """INSERT INTO SPECIALTUTORS(SUBJECT, FULLNAME, EMAIL, PHONENUMBER, USERID) VALUES (%s, %s, %s, %s, %s)"""
                cursor.execute(query, (tutor.subject, tutor.fullname, tutor.email, tutor.phonenumber, tutor.user_id))
                connection.commit()
            return redirect(url_for('site.SpecialTutor'))

If submitted form is update form, another set of operations is executed.

At the beginning, a database connection is created.

A SQL command to get current user's ID is created and used.

A hidden input that holds the current entry's ID is taken and assigned to a variable. After getting entry's ID, information is taken from form and if user did not submit any information in a field, that field's corresponding data is taken from database.

With every information is in place, a SQL command to update information is executed. After the operation is finishes, user is redirected to the page where they were.

.. code-block:: python

      elif formtype == "SpecialTutorUpdate":
            with dbapi2.connect(current_app.config['dsn']) as connection:
                  cursor = connection.cursor()  # prevented sql injection
                  statement = """SELECT ID FROM USERS WHERE (USERS.USERNAME = %s) AND (USERS.EMAIL = %s)"""
                  cursor.execute(statement, (username, email))
                  tutoruser_id = cursor.fetchone()
                  tutorid = request.form['tutor-id']

                  tutorsubject = request.form['SpecialTutorSubject']
                  if not tutorsubject:
                        statement = """SELECT SUBJECT FROM SPECIALTUTORS WHERE SPECIALTUTORS.ID = %s"""
                        cursor.execute(statement, tutorid)
                        tutorsubject = cursor.fetchone()

                  tutorname = request.form['SpecialTutorName']
                  if not tutorname:
                        statement = """SELECT FULLNAME FROM SPECIALTUTORS WHERE SPECIALTUTORS.ID = %s"""
                        cursor.execute(statement, tutorid)
                        tutorname = cursor.fetchone()

                  tutormail = request.form['SpecialTutorMail']
                  if not tutormail:
                        statement = """SELECT EMAIL FROM SPECIALTUTORS WHERE SPECIALTUTORS.ID = %s"""
                        cursor.execute(statement, tutorid)
                        tutormail = cursor.fetchone()

                  tutorphone = request.form['SpecialTutorPhone']
                  if not tutorphone:
                        statement = """SELECT PHONENUMBER FROM SPECIALTUTORS WHERE SPECIALTUTORS.ID = %s"""
                        cursor.execute(statement, tutorid)
                        tutorphone = cursor.fetchone()

                  statement = """UPDATE SPECIALTUTORS SET SUBJECT = %s, FULLNAME = %s, EMAIL = %s, PHONENUMBER = %s, USERID = %s WHERE SPECIALTUTORS.ID = %s"""
                  cursor.execute(statement,(tutorsubject, tutorname, tutormail, tutorphone, tutoruser_id, tutorid))
                  connection.commit()
                  return redirect(url_for('site.selected_special_tutor', tutorId=tutorid))

If user is only displaying the page, all of information is taken from database and displayed to user.

.. code-block:: python

      else:
            with dbapi2.connect(current_app.config['dsn']) as connection:
                  cursor = connection.cursor()
                  query = """SELECT SUBJECT, FULLNAME, SPECIALTUTORS.EMAIL, PHONENUMBER, USERS.USERNAME, SPECIALTUTORS.ID FROM SPECIALTUTORS, USERS WHERE (SPECIALTUTORS.USERID = USERS.ID)"""
                  cursor.execute(query)
                  specialtutors = cursor.fetchall()
            return render_template('special_tutor.html', specialtutors=specialtutors)


Special Students Page
---------------------

This page uses a class structure to manage inputs from users. It structure is shown below. It is placed at classes/special_student_class.py file.

.. code-block:: python

      class special_student:
            def __init__(self, subject, fullname, email, phonenumber, user_id):
                  self.subject = subject
                  self.fullname = fullname
                  self.email = email
                  self.phonenumber = phonenumber
                  self.user_id = user_id

This class have different methods to manipulate data.

One of these methods is used to get data of entry by using ID. This method returns an object with type of special_student by getting information from database.

.. code-block:: python

      def get_student_byId(studentId):
            with dbapi2.connect(current_app.config['dsn']) as connection:
                  cursor = connection.cursor()
                  statement = """SELECT * FROM SPECIALSTUDENTS WHERE SPECIALSTUDENTS.ID = %s"""
                  cursor.execute(statement, [studentId])
                  db_student = cursor.fetchall()
                  student = special_student(db_student[0][1], db_student[0][2], db_student[0][3], db_student[0][4], db_student[0][5])
                  student.id = db_student[0][0]
                  return student

Another method is used to delete entries from database. This method get ID of entry and deletes it from database table.

.. code-block:: python

      def delete_student_byId(studentId):
            with dbapi2.connect(current_app.config['dsn']) as connection:
                  cursor = connection.cursor()
                  statement = """DELETE FROM SPECIALSTUDENTS WHERE SPECIALSTUDENTS.ID = %s"""
                  cursor.execute(statement, [studentId])

At the beginning of special_student.py file, action's type decides next operations. If method is POST, it means user submitted a form. If method is GET, it means user is only displaying the page.

.. code-block:: python

      if request.method == "POST":

After that, if method is POST it is checked that if search box in top bar is used. If that search box is used, user is redirected to result page of their search.

.. code-block:: python

      if 'userSearchButton' in request.form: #if the search button is submitted
            session['search_username'] = request.form['usernameSearch']
            return redirect(url_for('site.SearchUserPage'))

If user did not use the search box, submitted form's type is taken via a hidden input to check form's purpose.

.. code-block:: python

      formtype = request.form['form-name']

After getting form type, information of current user is taken for later user.

.. code-block:: python

      username = current_user.get_username()
      email = current_user.get_email()
      name = current_user.get_name()
      surname = current_user.get_surname()

The code below is executed if user submits the form that creates new entry. At the beginning, data in the form is taken via request.form action. However, user have an option to leave name and mail blank. If they leave it blank, current user's information that taken before is used.

After that, psycopg2's database connection is used. A cursor that will be used for this database connection is created and SQL command is assigned to a statement. This statement pulls current user's ID from database and assigns it to a variable for later usage.

After getting all required information, an object is created for easier usage. A SQL statement is created and assigned to query variable. With database connection, query and object's data is submitted and a new row in database table is created.

After finishing work with database connection, it is closed. After all work is done, user is redirected to Special Student page to prevent submitting form for a second time by using refresh.

.. code-block:: python

      if formtype == "SpecialStudent":
            studentsubject = request.form['SpecialStudentSubject']
            studentname = request.form['SpecialStudentName']
            if not studentname:
                seq = {name, surname}
                studentname = " ".join(seq)
            studentmail = request.form['SpecialStudentMail']
            if not studentmail:
                studentmail = email
            studentphone = request.form['SpecialStudentPhone']

            with dbapi2.connect(current_app.config['dsn']) as connection:
                cursor = connection.cursor()
                statement = """SELECT ID FROM USERS WHERE (USERS.USERNAME = %s) AND (USERS.EMAIL = %s)"""
                cursor.execute(statement, (username, email))
                studentid = cursor.fetchone()

                student = special_student(studentsubject, studentname, studentmail, studentphone, studentid)
                query = """INSERT INTO SPECIALSTUDENTS(SUBJECT, FULLNAME, EMAIL, PHONENUMBER, USERID) VALUES (%s, %s, %s, %s, %s)"""
                cursor.execute(query, (student.subject, student.fullname, student.email, student.phonenumber, student.user_id))
                connection.commit()
            return redirect(url_for('site.SpecialStudent'))

If submitted form is update form, another set of operations is executed.

At the beginning, a database connection is created.

A SQL command to get current user's ID is created and used.

A hidden input that holds the current entry's ID is taken and assigned to a variable. After getting entry's ID, information is taken from form and if user did not submit any information in a field, that field's corresponding data is taken from database.

With every information is in place, a SQL command to update information is executed. After the operation is finishes, user is redirected to the page where they were.

.. code-block:: python

      elif formtype == "SpecialStudentUpdate":
            with dbapi2.connect(current_app.config['dsn']) as connection:
                  cursor = connection.cursor()  # prevented sql injection
                  statement = """SELECT ID FROM USERS WHERE (USERS.USERNAME = %s) AND (USERS.EMAIL = %s)"""
                  cursor.execute(statement, (username, email))
                  studentuser_id = cursor.fetchone()
                  studentid = request.form['student-id']

                  studentsubject = request.form['SpecialStudentSubject']
                  if not studentsubject:
                        statement = """SELECT SUBJECT FROM SPECIALSTUDENTS WHERE SPECIALSTUDENTS.ID = %s"""
                        cursor.execute(statement, studentid)
                        studentsubject = cursor.fetchone()

                  studentname = request.form['SpecialStudentName']
                  if not studentname:
                        statement = """SELECT FULLNAME FROM SPECIALSTUDENTS WHERE SPECIALSTUDENTS.ID = %s"""
                        cursor.execute(statement, studentid)
                        studentname = cursor.fetchone()

                  studentmail = request.form['SpecialStudentMail']
                  if not studentmail:
                        statement = """SELECT EMAIL FROM SPECIALSTUDENTS WHERE SPECIALSTUDENTS.ID = %s"""
                        cursor.execute(statement, studentid)
                        studentmail = cursor.fetchone()

                  studentphone = request.form['SpecialStudentPhone']
                  if not studentphone:
                        statement = """SELECT PHONENUMBER FROM SPECIALSTUDENTS WHERE SPECIALSTUDENTS.ID = %s"""
                        cursor.execute(statement, studentid)
                        studentphone = cursor.fetchone()

                  statement = """UPDATE SPECIALSTUDENTS SET SUBJECT = %s, FULLNAME = %s, EMAIL = %s, PHONENUMBER = %s, USERID = %s WHERE SPECIALSTUDENTS.ID = %s"""
                  cursor.execute(statement, (studentsubject, studentname, studentmail, studentphone, studentuser_id, studentid))
                  connection.commit()
                  return redirect(url_for('site.selected_special_student', studentId=studentid))

If user is only displaying the page, all of information is taken from database and displayed to user.

.. code-block:: python

      else:
            with dbapi2.connect(current_app.config['dsn']) as connection:
                  cursor = connection.cursor()
                  query = """SELECT SUBJECT, FULLNAME, SPECIALSTUDENTS.EMAIL, PHONENUMBER, USERS.USERNAME, SPECIALSTUDENTS.ID FROM SPECIALSTUDENTS, USERS WHERE (SPECIALSTUDENTS.USERID = USERS.ID)"""
                  cursor.execute(query)
                  specialstudents = cursor.fetchall()
            return render_template('special_student.html', specialstudents=specialstudents)

Lost Stuff Page
---------------------

This page uses a class structure to manage inputs from users. It structure is shown below. It is placed at classes/lost_stuff_class.py file.

.. code-block:: python

      class lost_stuff:
            def __init__(self, lostdesc, lostlocation, lostdate, lostownername, lostmail, lostphone, lostuser_id):
                  self.description = lostdesc
                  self.location = lostlocation
                  self.date = lostdate
                  self.ownername = lostownername
                  self.mail = lostmail
                  self.phone = lostphone
                  self.user_id = lostuser_id

This class have different methods to manipulate data.

One of these methods is used to get data of entry by using ID. This method returns an object with type of lost_stuff by getting information from database.

.. code-block:: python

      def get_lost_byId(lostId):
            with dbapi2.connect(current_app.config['dsn']) as connection:
                  cursor = connection.cursor()
                  statement = """SELECT * FROM LOSTSTUFF WHERE LOSTSTUFF.ID = %s"""
                  cursor.execute(statement, [lostId])
                  db_lost = cursor.fetchall()
                  lost = lost_stuff(db_lost[0][1], db_lost[0][2], db_lost[0][3], db_lost[0][4], db_lost[0][5], db_lost[0][6], db_lost[0][7])
                  lost.id = db_lost[0][0]
                  return lost

Another method is used to delete entries from database. This method get ID of entry and deletes it from database table.

.. code-block:: python

      def delete_lost_byId(lostId):
            with dbapi2.connect(current_app.config['dsn']) as connection:
                  cursor = connection.cursor()
                  statement = """DELETE FROM LOSTSTUFF WHERE LOSTSTUFF.ID = %s"""
                  cursor.execute(statement, [lostId])

At the beginning of lost_stuff.py file, action's type decides next operations. If method is POST, it means user submitted a form. If method is GET, it means user is only displaying the page.

.. code-block:: python

      if request.method == "POST":

After that, if method is POST it is checked that if search box in top bar is used. If that search box is used, user is redirected to result page of their search.

.. code-block:: python

      if 'userSearchButton' in request.form: #if the search button is submitted
            session['search_username'] = request.form['usernameSearch']
            return redirect(url_for('site.SearchUserPage'))

If user did not use the search box, submitted form's type is taken via a hidden input to check form's purpose.

.. code-block:: python

      formtype = request.form['form-name']

After getting form type, information of current user is taken for later user.

.. code-block:: python

      username = current_user.get_username()
      email = current_user.get_email()
      name = current_user.get_name()
      surname = current_user.get_surname()

The code below is executed if user submits the form that creates new entry. At the beginning, data in the form is taken via request.form action. However, user have an option to leave name and mail blank. If they leave it blank, current user's information that taken before is used.

After that, psycopg2's database connection is used. A cursor that will be used for this database connection is created and SQL command is assigned to a statement. This statement pulls current user's ID from database and assigns it to a variable for later usage.

After getting all required information, an object is created for easier usage. A SQL statement is created and assigned to query variable. With database connection, query and object's data is submitted and a new row in database table is created.

After finishing work with database connection, it is closed. After all work is done, user is redirected to Special Student page to prevent submitting form for a second time by using refresh.

.. code-block:: python

      if formtype == "LostSomething":
            lostdesc = request.form['LostSomethingDescription']
            lostlocation = request.form['LostSomethingPossibleLocation']
            lostdate = request.form['LostSomethingDate']
            lostownername = request.form['LostSomethingOwnerName']
            if not lostownername:
                seq = {name, surname}
                lostownername = " ".join(seq)
            lostmail = request.form['LostSomethingOwnerMail']
            if not lostmail:
                lostmail = email
            lostphone = request.form['LostSomethingOwnerPhone']

            with dbapi2.connect(current_app.config['dsn']) as connection:
                cursor = connection.cursor()#prevented sql injection
                statement = """SELECT ID FROM USERS WHERE (USERS.USERNAME = %s) AND (USERS.EMAIL = %s)"""
                cursor.execute(statement, (username, email))
                lostuser_id = cursor.fetchone()

                lost = lost_stuff(lostdesc, lostlocation, lostdate, lostownername, lostmail, lostphone, lostuser_id)
                query = """INSERT INTO LOSTSTUFF(STUFFDESC, POSSIBLELOC, POSSIBLEDATE, OWNERNAME, OWNERMAIL, OWNERPHONE, USERID) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
                cursor.execute(query, (lost.description, lost.location, lost.date, lost.ownername, lost.mail, lost.phone, lost.user_id))
                connection.commit()
            return redirect(url_for('site.LostStuff'))

If submitted form is update form, another set of operations is executed.

At the beginning, a database connection is created.

A SQL command to get current user's ID is created and used.

A hidden input that holds the current entry's ID is taken and assigned to a variable. After getting entry's ID, information is taken from form and if user did not submit any information in a field, that field's corresponding data is taken from database.

With every information is in place, a SQL command to update information is executed. After the operation is finishes, user is redirected to the page where they were.

.. code-block:: python

      elif formtype == "LostSomethingUpdate":
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

If user is only displaying the page, all of information is taken from database and displayed to user.

.. code-block:: python

      else:
            with dbapi2.connect(current_app.config['dsn']) as connection:
                  cursor = connection.cursor()
                  query = """SELECT STUFFDESC, POSSIBLELOC, POSSIBLEDATE, OWNERNAME, OWNERMAIL, OWNERPHONE, USERS.USERNAME, LOSTSTUFF.ID FROM LOSTSTUFF, USERS WHERE (LOSTSTUFF.USERID = USERS.ID)"""
                  cursor.execute(query)
                  lostitems = cursor.fetchall()
            return render_template('lost_stuff.html', lostitems=lostitems)

Found Stuff Page
---------------------

This page uses a class structure to manage inputs from users. It structure is shown below. It is placed at classes/found_stuff_class.py file.

.. code-block:: python

      def __init__(self, founddesc, foundlocation, founddate, foundname, foundmail, foundphone, founduser_id):
            self.description = founddesc
            self.location = foundlocation
            self.date = founddate
            self.name = foundname
            self.mail = foundmail
            self.phone = foundphone
            self.user_id = founduser_id

This class have different methods to manipulate data.

One of these methods is used to get data of entry by using ID. This method returns an object with type of lost_stuff by getting information from database.

.. code-block:: python

      def get_found_byId(foundId):
            with dbapi2.connect(current_app.config['dsn']) as connection:
                  cursor = connection.cursor()
                  statement = """SELECT * FROM FOUNDSTUFF WHERE FOUNDSTUFF.ID = %s"""
                  cursor.execute(statement, [foundId])
                  db_found = cursor.fetchall()
                  found = found_stuff(db_found[0][1], db_found[0][2], db_found[0][3], db_found[0][4], db_found[0][5], db_found[0][6], db_found[0][7])
                  found.id = db_found[0][0]
                  return found

Another method is used to delete entries from database. This method get ID of entry and deletes it from database table.

.. code-block:: python

      def delete_found_byId(foundId):
            with dbapi2.connect(current_app.config['dsn']) as connection:
                  cursor = connection.cursor()
                  statement = """DELETE FROM FOUNDSTUFF WHERE FOUNDSTUFF.ID = %s"""
                  cursor.execute(statement, [foundId])

At the beginning of found_stuff.py file, action's type decides next operations. If method is POST, it means user submitted a form. If method is GET, it means user is only displaying the page.

.. code-block:: python

      if request.method == "POST":

After that, if method is POST it is checked that if search box in top bar is used. If that search box is used, user is redirected to result page of their search.

.. code-block:: python

      if 'userSearchButton' in request.form: #if the search button is submitted
            session['search_username'] = request.form['usernameSearch']
            return redirect(url_for('site.SearchUserPage'))

If user did not use the search box, submitted form's type is taken via a hidden input to check form's purpose.

.. code-block:: python

      formtype = request.form['form-name']

After getting form type, information of current user is taken for later user.

.. code-block:: python

      username = current_user.get_username()
      email = current_user.get_email()
      name = current_user.get_name()
      surname = current_user.get_surname()

The code below is executed if user submits the form that creates new entry. At the beginning, data in the form is taken via request.form action. However, user have an option to leave name and mail blank. If they leave it blank, current user's information that taken before is used.

After that, psycopg2's database connection is used. A cursor that will be used for this database connection is created and SQL command is assigned to a statement. This statement pulls current user's ID from database and assigns it to a variable for later usage.

After getting all required information, an object is created for easier usage. A SQL statement is created and assigned to query variable. With database connection, query and object's data is submitted and a new row in database table is created.

After finishing work with database connection, it is closed. After all work is done, user is redirected to Special Student page to prevent submitting form for a second time by using refresh.

.. code-block:: python

      if formtype == "FoundSomething":
            founddesc = request.form['FoundSomethingDescription']
            foundlocation = request.form['FoundSomethingCurrentLocation']
            founddate = request.form['FoundSomethingDate']
            foundname = request.form['FoundSomethingFinderName']
            if not foundname:
                seq = {name, surname}
                foundname = " ".join(seq)
            foundmail = request.form['FoundSomethingFinderMail']
            if not foundmail:
                foundmail = email
            foundphone = request.form['FoundSomethingFinderPhone']

            with dbapi2.connect(current_app.config['dsn']) as connection:
                cursor = connection.cursor()#prevented sql injection
                statement = """SELECT ID FROM USERS WHERE (USERS.USERNAME = %s) AND (USERS.EMAIL = %s)"""
                cursor.execute(statement, (username, email))
                founduser_id = cursor.fetchone()

                found = found_stuff(founddesc, foundlocation, founddate, foundname, foundmail, foundphone, founduser_id)
                query = """INSERT INTO FOUNDSTUFF(STUFFDESC, CURRENTLOC, FINDINGDATE, FOUNDERNAME, FOUNDERMAIL, FOUNDERPHONE, USERID) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
                cursor.execute(query, (found.description, found.location, found.date, found.name, found.mail, found.phone, found.user_id))
                connection.commit()
                return redirect(url_for('site.FoundStuff'))

If submitted form is update form, another set of operations is executed.

At the beginning, a database connection is created.

A SQL command to get current user's ID is created and used.

A hidden input that holds the current entry's ID is taken and assigned to a variable. After getting entry's ID, information is taken from form and if user did not submit any information in a field, that field's corresponding data is taken from database.

With every information is in place, a SQL command to update information is executed. After the operation is finishes, user is redirected to the page where they were.

.. code-block:: python

      elif formtype == "FoundSomethingUpdate":
            with dbapi2.connect(current_app.config['dsn']) as connection:
                cursor = connection.cursor()#prevented sql injection
                statement = """SELECT ID FROM USERS WHERE (USERS.USERNAME = %s) AND (USERS.EMAIL = %s)"""
                cursor.execute(statement, (username, email))
                founduser_id = cursor.fetchone()
                foundid = request.form['found-id']

                founddesc = request.form['FoundSomethingDescription']
                print("-", founddesc, "-\n")
                if not founddesc:
                    statement = """SELECT STUFFDESC FROM FOUNDSTUFF WHERE FOUNDSTUFF.ID = %s"""
                    cursor.execute(statement, foundid)
                    founddesc = cursor.fetchone()

                foundlocation = request.form['FoundSomethingCurrentLocation']
                print("-", foundlocation, "-\n")
                if not foundlocation:
                    statement = """SELECT CURRENTLOC FROM FOUNDSTUFF WHERE FOUNDSTUFF.ID = %s"""
                    cursor.execute(statement, foundid)
                    foundlocation = cursor.fetchone()

                founddate = request.form['FoundSomethingDate']
                if not founddate:
                    statement = """SELECT FINDINGDATE FROM FOUNDSTUFF WHERE FOUNDSTUFF.ID = %s"""
                    cursor.execute(statement,foundid)
                    founddate = cursor.fetchone()

                foundname = request.form['FoundSomethingFinderName']
                print("-", foundname, "-\n")
                if not foundname:
                    statement = """SELECT FOUNDERNAME FROM FOUNDSTUFF WHERE FOUNDSTUFF.ID = %s"""
                    cursor.execute(statement, foundid)
                    foundname = cursor.fetchone()

                foundmail = request.form['FoundSomethingFinderMail']
                print("-", foundmail, "-\n")
                if not foundmail:
                    statement = """SELECT FOUNDERMAIL FROM FOUNDSTUFF WHERE FOUNDSTUFF.ID = %s"""
                    cursor.execute(statement, foundid)
                    foundmail = cursor.fetchone()

                foundphone = request.form['FoundSomethingFinderPhone']
                print("-", foundphone, "-\n")
                if not foundphone:
                    statement = """SELECT FOUNDERPHONE FROM FOUNDSTUFF WHERE FOUNDSTUFF.ID = %s"""
                    cursor.execute(statement, foundid)
                    foundphone = cursor.fetchone()

                statement = """UPDATE FOUNDSTUFF SET STUFFDESC=%s, CURRENTLOC=%s, FINDINGDATE=%s, FOUNDERNAME=%s, FOUNDERMAIL=%s, FOUNDERPHONE=%s, USERID=%s WHERE FOUNDSTUFF.ID=%s"""
                cursor.execute(statement, (founddesc, foundlocation, founddate, foundname, foundmail, foundphone, founduser_id, foundid))
                connection.commit()
                return redirect(url_for('site.selected_found_stuff', foundId=foundid))

If user is only displaying the page, all of information is taken from database and displayed to user.

.. code-block:: python

      else:
            with dbapi2.connect(current_app.config['dsn']) as connection:
                  cursor = connection.cursor()
                  query = """SELECT STUFFDESC, CURRENTLOC, FINDINGDATE, FOUNDERNAME, FOUNDERMAIL, FOUNDERPHONE, USERS.USERNAME, FOUNDSTUFF.ID FROM FOUNDSTUFF, USERS WHERE (FOUNDSTUFF.USERID = USERS.ID)"""
                  cursor.execute(query)
                  founditems = cursor.fetchall()
            return render_template('found_stuff.html', founditems=founditems)