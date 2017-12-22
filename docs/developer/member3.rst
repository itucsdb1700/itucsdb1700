Parts Implemented by Adil Furkan Ekici
======================================

Sharing House page is related to DATASHAREDHOUSE table.

Searching House page is related to DATASEARCHINGHOUSE table.

Sharing Books page is related to SHAREDBOOKS table

Sharing Lesson Notes page is related to SHAREDLESSONNOTES table.



Sharing House Page
------------------

There is also an class for DATASHAREDHOUSE table

.. code-block:: python

    class sharingHouseAnnouncement:
        def __init__(self,location,rentPrice,numberOfPeople,numberOfRoom,description,currentuser_id):
            self.LocationOfSharingHouse = location
            self.RentPriceOfSharingHouse = rentPrice
            self.NumberOfPeopleInSharingHouse = numberOfPeople
            self.NumberOfSharingHouseRoom = numberOfRoom
            self.DescriptionOfSharingHouse  = description
            self.id_ownerOfSharingHouseAnnouncement = currentuser_id


Users can add sharing house announcement in Sharing House page with modal form.You can see the corresponding code below

.. code-block:: python

      Location = request.form['InputLocationOfSharingHouse']
      RentPrice = request.form['InputRentPriceOfSharingHouse']
      NumberOfPeople = request.form['InputnumberOfPeopleInHouse']
      NumberOfRoom = request.form['InputNumberOfRoomforSharingHouse']
      Description = request.form['InputDescriptionOfSharingHouse']

Website can take id for user who created the sharing house announcement. You can see the corresponding code below

.. code-block:: python

      cursor = connection.cursor()#prevented sql injection
      statement = """SELECT ID FROM USERS WHERE(USERS.USERNAME = %s) AND(USERS.EMAIL = %s)"""
      cursor.execute(statement, (username,email))
      currentuser_id = cursor.fetchone()

A class is created with taken information from users.You can see the corresponding class below

.. code-block:: python

       sharingHouseAd = sharingHouseAnnouncement(Location,RentPrice,NumberOfPeople,NumberOfRoom,Description,currentuser_id)

These information is added to database with query.You can see the corresponding query below

.. code-block:: python

      query ="""INSERT INTO DATASHAREDHOUSE(LOCATION, RENTPRICE, NUMBEROFPEOPLE, NUMBEROFROOM, DESCRIPTION, USERID) VALUES (%s, %s, %s, %s, %s, %s)"""
      cursor.execute(query, (sharingHouseAd.LocationOfSharingHouse, sharingHouseAd.RentPriceOfSharingHouse, sharingHouseAd.NumberOfPeopleInSharingHouse,
                              sharingHouseAd.NumberOfSharingHouseRoom, sharingHouseAd.DescriptionOfSharingHouse,sharingHouseAd.id_ownerOfSharingHouseAnnouncement))


Users can update announcement in Sharing House Details page.Users can edit information with modal form in update process. If users did not want change some information. These information will remain the same.

You can see the corresponding code below.

.. code-block:: python

      Location = request.form['InputLocationOfSharingHouse']
      if not Location:
           statement = """SELECT LOCATION FROM DATASHAREDHOUSE WHERE DATASHAREDHOUSE.ID = %s"""
           cursor.execute(statement, sharingHouseid)
           Location = cursor.fetchone()

      RentPrice = request.form['InputRentPriceOfSharingHouse']
      if not RentPrice:
           statement = """SELECT RENTPRICE FROM DATASHAREDHOUSE WHERE DATASHAREDHOUSE.ID = %s"""
           cursor.execute(statement, sharingHouseid)
           RentPrice = cursor.fetchone()

      NumberOfPeople = request.form['InputnumberOfPeopleInHouse']
      if not NumberOfPeople:
           statement = """SELECT NUMBEROFPEOPLE FROM DATASHAREDHOUSE WHERE DATASHAREDHOUSE.ID = %s"""
           cursor.execute(statement, sharingHouseid)
           NumberOfPeople = cursor.fetchone()

      NumberOfRoom = request.form['InputNumberOfRoomforSharingHouse']
      if not NumberOfRoom:
           statement = """SELECT NUMBEROFROOM FROM DATASHAREDHOUSE WHERE DATASHAREDHOUSE.ID = %s"""
           cursor.execute(statement, sharingHouseid)
           NumberOfRoom = cursor.fetchone()

      Description = request.form['InputDescriptionOfSharingHouse']
      if not Description:
           statement = """SELECT DESCRIPTION FROM DATASHAREDHOUSE WHERE DATASHAREDHOUSE.ID = %s"""
           cursor.execute(statement, sharingHouseid)
           Description = cursor.fetchone()

These announcement is updated on database.You can see the corresponding code below.

.. code-block:: python

      statement = """UPDATE DATASHAREDHOUSE SET LOCATION=%s, RENTPRICE=%s, NUMBEROFPEOPLE=%s, NUMBEROFROOM=%s, DESCRIPTION=%s, USERID=%s WHERE DATASHAREDHOUSE.ID=%s"""
      cursor.execute(statement,(Location, RentPrice, NumberOfPeople, NumberOfRoom, Description, sharingUser_id, sharingHouseid))
      connection.commit()

If user want to delete own announcement or admin want to this, User can delete announcement with delete button in Sharing House details page.You can see the corresponding query below.

.. code-block:: python

       statement = """DELETE FROM DATASHAREDHOUSE WHERE DATASHAREDHOUSE.ID = %s"""

.. raw:: latex

    \newpage

Searching House Page
--------------------

There is also an class for DATASEARCHEDHOUSE table

.. code-block::python

      class searchingHouseAnnouncement:
            def __init__(self,location,mixRent,maxRent,description,currentuser_id):
                  self.LocationOfSearchingHouse = location
                  self.MinRentPriceOfSearchingHouse = mixRent
                  self.MaxRentPriceOfSearchingHouse = maxRent
                  self.DescriptionOfSearchingHouse = description
                  self.id_ownerOfSearchingHouseAnnouncement = currentuser_id



Users can add searching house announcement in Searching House page with modal form.You can see the corresponding code below

.. code-block:: python

      Location = request.form['InputLocationOfSearchingHouse']
      MinRent = request.form['InputMinRentPriceOfSearchingHouse']
      MaxRent = request.form['InputMaxRentPriceOfSearchingHouse']
      Description = request.form['InputDescriptionOfSearchingHouse']

Website can take id for user who created the searching house announcement. You can see the corresponding code below

.. code-block:: python

            cursor = connection.cursor()
            statement = """SELECT ID FROM USERSWHERE(USERS.USERNAME = %s)AND(USERS.EMAIL = %s)"""
            cursor.execute(statement, (username,email))
            currentuser_id = cursor.fetchone())

A class is created with taken information from users.You can see the corresponding class below

.. code-block:: python

      searchingHouseAd = searchingHouseAnnouncement(Location,MinRent,MaxRent,Description,currentuser_id)

These information is added to database with query.You can see the corresponding query below

.. code-block:: python

      query = """INSERT INTO DATASEARCHEDHOUSE(LOCATION, MINRENTPRICE, MAXRENTPRICE,DESCRIPTION,USERID)VALUES (%s,%s,%s,%s,%s)"""
      cursor.execute(query, (searchingHouseAd.LocationOfSearchingHouse, searchingHouseAd.MinRentPriceOfSearchingHouse, searchingHouseAd.MaxRentPriceOfSearchingHouse,
                              searchingHouseAd.DescriptionOfSearchingHouse,searchingHouseAd.id_ownerOfSearchingHouseAnnouncement))

Users can update announcement in Searching House Details page.Users can edit information with modal form in update process. If users did not want change some information. These information will remain the same.

You can see the corresponding code below.

.. code-block:: python

       Location = request.form['InputLocationOfSearchingHouse']
       if not Location:
           statement = """SELECT LOCATION FROM DATASEARCHEDHOUSE WHERE DATASEARCHEDHOUSE.ID = %s"""
           cursor.execute(statement, searchingHouseid)
           Location = cursor.fetchone()

       MinRent = request.form['InputMinRentPriceOfSearchingHouse']
       if not MinRent:
           statement = """SELECT MINRENT FROM DATASEARCHEDHOUSE WHERE DATASEARCHEDHOUSE.ID = %s"""
           cursor.execute(statement, searchingHouseid)
           MinRent = cursor.fetchone()

       MaxRent = request.form['InputMaxRentPriceOfSearchingHouse']
       if not MaxRent:
           statement = """SELECT MAXRENT FROM DATASEARCHEDHOUSE WHERE DATASEARCHEDHOUSE.ID = %s"""
           cursor.execute(statement, searchingHouseid)
           MaxRent = cursor.fetchone()

       Description = request.form['InputDescriptionOfSearchingHouse']
       if not Description:
           statement = """SELECT DESCRIPTION FROM DATASEARCHEDHOUSE WHERE DATASEARCHEDHOUSE.ID = %s"""
           cursor.execute(statement, searchingHouseid)
           Description = cursor.fetchone()

These announcement is updated on database.You can see the corresponding code below.

.. code-block:: python

      statement = """UPDATE DATASEARCHEDHOUSE SET LOCATION=%s, MINRENTPRICE=%s, MAXRENTPRICE=%s, DESCRIPTION=%s, USERID=%s WHERE DATASEARCHEDHOUSE.ID=%s"""
      cursor.execute(statement,(Location, MinRent, MaxRent, Description, searchingHouseUser_id, searchingHouseid))
      connection.commit()

If user want to delete own announcement or admin want to this, User can delete announcement with delete button in Searching House details page.You can see the corresponding query below.

.. code-block:: python

      statement = """DELETE FROM DATASEARCHEDHOUSE WHERE DATASEARCHEDHOUSE.ID = %s"""

.. raw:: latex

    \newpage

Book Sharing Page
-----------------

There is also an class for SHAREDBOOKS table

.. code-block:: python

      class sharingBooksAnnouncement:
            def __init__(self,NameOfBook,LessonName,LessonCode,TypeOfShare,Price,currentuser_id):
            self.NameOFSharingBooks = NameOfBook
            self.LessonNameOfSharingBooks = LessonName
            self.LessonCodeOfSharingBooks = LessonCode
            self.TypeOfSharingBooks = TypeOfShare
            self.PriceOFSharingBooks = Price
            self.id_ownerOfSharingBooks = currentuser_id


Users can add sharing book announcement in Sharing Books page with modal form.You can see the corresponding code below

.. code-block:: python

      NameOfBook = request.form['InputNameOfSharedBook']
      LessonName = request.form['InputLessonNameOfShareBook']
      LessonCode = request.form['InputLessonCodeOfShareBook']
      TypeOfShare = request.form['InputTypeOfSharedBooks']
      if(request.form['InputPriceOfShareBook']):
         Price = request.form['InputPriceOfShareBook']
      else:
         Price = None

Website can take id for user who created the sharing book announcement. You can see the corresponding code below

.. code-block:: python

            cursor = connection.cursor()
            statement = """SELECT ID FROM USERSWHERE(USERS.USERNAME = %s)AND(USERS.EMAIL = %s)"""
            cursor.execute(statement, (username,email))
            currentuser_id = cursor.fetchone())

A class is created with taken information from users.You can see the corresponding class below

.. code-block:: python

     sharedBooksAd = sharingBooksAnnouncement(NameOfBook,LessonName,LessonCode,TypeOfShare,Price,currentuser_id)

These information is added to database with query.You can see the corresponding query below

.. code-block:: python

      query = """INSERT INTO SHAREDBOOKS(NAMEOFBOOK, LESSONNAME, LESSONCODE,TYPEOFSHARE,PRICE,USERID)VALUES (%s,%s,%s,%s,%s,%s)"""
      cursor.execute(query, (sharedBooksAd.NameOFSharingBooks,sharedBooksAd.LessonNameOfSharingBooks,
                             sharedBooksAd.LessonCodeOfSharingBooks,sharedBooksAd.TypeOfSharingBooks,
                             sharedBooksAd.PriceOFSharingBooks,sharedBooksAd.id_ownerOfSharingBooks))
      connection.commit()

Users can update announcement in Sharing Books Details page.Users can edit information with modal form in update process. If users did not want change some information. These information will remain the same.

You can see the corresponding code below.

.. code-block:: python

            NameOfBook = request.form['InputNameOfSharedBook']
            if not NameOfBook:
               statement = """SELECT NAMEOFBOOK FROM SHAREDBOOKS WHERE SHAREDBOOKS.ID = %s"""
               cursor.execute(statement, sharingBookid)
               NameOfBook = cursor.fetchone()

            LessonName = request.form['InputLessonNameOfShareBook']
            if not LessonName:
               statement = """SELECT LESSONNAME FROM SHAREDBOOKS WHERE SHAREDBOOKS.ID = %s"""
               cursor.execute(statement, sharingBookid)
               LessonName = cursor.fetchone()

            LessonCode = request.form['InputLessonCodeOfShareBook']
            if not LessonCode:
               statement = """SELECT LESSONCODE FROM SHAREDBOOKS WHERE SHAREDBOOKS.ID = %s"""
               cursor.execute(statement, sharingBookid)
               LessonCode = cursor.fetchone()

            TypeOfShare = request.form['InputTypeOfSharedBooks']
            if not TypeOfShare:
               statement = """SELECT TYPEOFSHARE FROM SHAREDBOOKS WHERE SHAREDBOOKS.ID = %s"""
               cursor.execute(statement, sharingBookid)
               TypeOfShare = cursor.fetchone()

            Price = request.form['InputPriceOfShareBook']
            if not Price:
               statement = """SELECT PRICE FROM SHAREDBOOKS WHERE SHAREDBOOKS.ID = %s"""
               cursor.execute(statement, sharingBookid)
               Price = cursor.fetchone()

These announcement is updated on database.You can see the corresponding code below.

.. code-block:: python

       statement = """UPDATE SHAREDBOOKS SET NAMEOFBOOK=%s, LESSONNAME=%s, LESSONCODE=%s, TYPEOFSHARE=%s, PRICE=%s, USERID=%s WHERE SHAREDBOOKS.ID=%s"""
       cursor.execute(statement,(NameOfBook, LessonName, LessonCode, TypeOfShare, Price, sharingUser_id,sharingBookid))
       connection.commit()

If user want to delete own announcement or admin want to this, User can delete announcement with delete button in Sharing Books Details page.You can see the corresponding query below.

.. code-block:: python

      statement = """DELETE FROM SHAREDBOOKS WHERE SHAREDBOOKS.ID = %s"""

.. raw:: latex

    \newpage


Note Sharing Page
-----------------

There is also an class for SHAREDLESSONNOTES table

.. code-block:: python

      class sharingLessonNotesAnnouncement:
            def __init__(self,NameOfLessonNote,LessonName,LessonCode,TeacherName,currentuser_id):
                 self.NameOFSharingLessonNote = NameOfLessonNote
                 self.LessonNameOfSharingLessonNote = LessonName
                 self.LessonCodeOfSharingLessonNote = LessonCode
                 self.TeacherNameOFSharingLessonNote = TeacherName
                 self.id_ownerOfSharingLessonNote = currentuser_id

Users can add sharing book announcement in Sharing Lesson Notes page with modal form.You can see the corresponding code below

.. code-block:: python

       NameOfLessonNote = request.form['InputNameOfSharedLessonNote']
       TeacherName = request.form['InputTeacherNameofSharedLessonNote']
       LessonName = request.form['InputLessonNameOfShareLessonNote']
       LessonCode = request.form['InputLessonCodeOfShareLessonNote']

Website can take id for user who created the sharing lesson notes announcement. You can see the corresponding code below

.. code-block:: python

            cursor = connection.cursor()
            statement = """SELECT ID FROM USERSWHERE(USERS.USERNAME = %s)AND(USERS.EMAIL = %s)"""
            cursor.execute(statement, (username,email))
            currentuser_id = cursor.fetchone())

A class is created with taken information from users.You can see the corresponding class below

.. code-block:: python

     sharedBooksAd = sharingBooksAnnouncement(NameOfBook,LessonName,LessonCode,TypeOfShare,Price,currentuser_id)

These information is added to database with query.You can see the corresponding query below

.. code-block:: python

      query = """INSERT INTO SHAREDLESSONNOTES(NAMEOFNOTES, LESSONNAME, LESSONCODE,TEACHERNAME,USERID)VALUES (%s,%s,%s,%s,%s)"""
      cursor.execute(query, (sharedLessonNotesAd.NameOFSharingLessonNote,sharedLessonNotesAd.LessonNameOfSharingLessonNote,sharedLessonNotesAd.LessonCodeOfSharingLessonNote,
                             sharedLessonNotesAd.TeacherNameOFSharingLessonNote,sharedLessonNotesAd.id_ownerOfSharingLessonNote))
      connection.commit()

Users can update announcement in Sharing Lesson Notes Details page.Users can edit information with modal form in update process. If users did not want change some information. These information will remain the same.

You can see the corresponding code below.

.. code-block:: python

            NameOfLessonNote = request.form['InputNameOfSharedLessonNote']
            if not NameOfLessonNote:
                statement = """SELECT NAMEOFNOTES FROM SHAREDLESSONNOTES WHERE SHAREDLESSONNOTES.ID = %s"""
                cursor.execute(statement, sharingLessonNotesid)
                NameOfLessonNote = cursor.fetchone()

            TeacherName = request.form['InputTeacherNameofSharedLessonNote']
            if not TeacherName:
                statement = """SELECT TEACHERNAME FROM SHAREDLESSONNOTES WHERE SHAREDLESSONNOTES.ID = %s"""
                cursor.execute(statement, sharingLessonNotesid)
                TeacherName = cursor.fetchone()

            LessonName = request.form['InputLessonNameOfShareLessonNote']
            if not LessonName:
                statement = """SELECT LESSONNAME FROM SHAREDLESSONNOTES WHERE SHAREDLESSONNOTES.ID = %s"""
                cursor.execute(statement, sharingLessonNotesid)
                LessonName = cursor.fetchone()

            LessonCode = request.form['InputLessonCodeOfShareLessonNote']
            if not LessonCode:
                statement = """SELECT LESSONCODE FROM SHAREDLESSONNOTES WHERE SHAREDLESSONNOTES.ID = %s"""
                cursor.execute(statement, sharingLessonNotesid)
                LessonCode = cursor.fetchone()

These announcement is updated on database.You can see the corresponding code below.

.. code-block:: python

       statement = """UPDATE SHAREDLESSONNOTES SET NAMEOFNOTES=%s, LESSONNAME=%s, LESSONCODE=%s, TEACHERNAME=%s, USERID=%s WHERE SHAREDLESSONNOTES.ID=%s"""
       cursor.execute(statement,(NameOfLessonNote, LessonName, LessonCode,  TeacherName, sharingUser_id, sharingLessonNotesid))
       connection.commit()

If user want to delete own announcement or admin want to this, User can delete announcement with delete button in Sharing Lesson Notes Details page.You can see the corresponding query below.

.. code-block:: python

      statement = """DELETE FROM SHAREDLESSONNOTES WHERE SHAREDLESSONNOTES.ID = %s"""

.. raw:: latex

    \newpage