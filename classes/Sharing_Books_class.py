from flask import current_app
from flask_login import UserMixin
import psycopg2 as dbapi2

class sharingBooksAnnouncement:
    def __init__(self,NameOfBook,LessonName,LessonCode,TypeOfShare,Price,currentuser_id):
        self.NameOFSharingBooks = NameOfBook
        self.LessonNameOfSharingBooks = LessonName
        self.LessonCodeOfSharingBooks = LessonCode
        self.TypeOfSharingBooks = TypeOfShare
        self.PriceOFSharingBooks = Price
        self.id_ownerOfSharingBooks = currentuser_id

    def delete_sharingBooksAnnouncement_byId(id):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            statement = """DELETE FROM SHAREDBOOKS WHERE SHAREDBOOKS.ID = %s"""
            cursor.execute(statement, [id])