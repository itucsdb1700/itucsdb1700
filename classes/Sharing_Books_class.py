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

    def get_NameOfSharingBooks(self):
        return self.NameOFSharingBooks
    def get_LessonNameOfSharingBooks(self):
        return self.LessonNameOfSharingBooks
    def get_LessonCodeOfSharingBooks(self):
        return self.LessonCodeOfSharingBooks
    def get_TypeOfSharingBooks(self):
        return self.TypeOfSharingBooks
    def get_PriceOFSharingBooks(self):
        return self.PriceOFSharingBooks
    def get_id_ownerOfSharingBooks(self):
        return self.id_ownerOfSharingBooks

    def get_sharingBooksAnnouncementt_byId(id):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            statement = """SELECT * FROM SHAREDBOOKS WHERE SHAREDBOOKS.ID = %s"""
            cursor.execute(statement, [id])
            db_Book = cursor.fetchall()
            sharingBooks = sharingBooksAnnouncement(db_Book[0][1], db_Book[0][2], db_Book[0][3], db_Book[0][4], db_Book[0][5], db_Book[0][6])
            sharingBooks.id = db_Book[0][0]
            return sharingBooks

    def delete_sharingBooksAnnouncement_byId(id):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            statement = """DELETE FROM SHAREDBOOKS WHERE SHAREDBOOKS.ID = %s"""
            cursor.execute(statement, [id])