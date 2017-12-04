from flask import current_app
from flask_login import UserMixin
import psycopg2 as dbapi2

class sharingLessonNotesAnnouncement:
    def __init__(self,NameOfLessonNote,LessonName,LessonCode,TeacherName,currentuser_id):
        self.NameOFSharingLessonNote = NameOfLessonNote
        self.LessonNameOfSharingLessonNote = LessonName
        self.LessonCodeOfSharingLessonNote = LessonCode
        self.TeacherNameOFSharingLessonNote = TeacherName
        self.id_ownerOfSharingLessonNote = currentuser_id

    def get_NameOFSharingLessonNote(self):
        return self.NameOFSharingLessonNote
    def get_LessonNameOfSharingLessonNote(self):
        return self.LessonNameOfSharingLessonNote
    def get_LessonCodeOfSharingLessonNote(self):
        return self.LessonCodeOfSharingLessonNote
    def get_TeacherNameOFSharingLessonNote(self):
        return self.TeacherNameOFSharingLessonNote
    def get_id_ownerOfSharingLessonNote(self):
        return self.id_ownerOfSharingLessonNote

    def get_SharingLessonNotes_byId(id):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            statement = """SELECT * FROM SHAREDLESSONNOTES WHERE SHAREDLESSONNOTES.ID = %s"""
            cursor.execute(statement, [id])
            db_SharingLessonNotes = cursor.fetchall()
            SharingLessonNotes = sharingLessonNotesAnnouncement(db_SharingLessonNotes[0][1], db_SharingLessonNotes[0][2], db_SharingLessonNotes[0][3], db_SharingLessonNotes[0][4], db_SharingLessonNotes[0][5])
            SharingLessonNotes.id = db_SharingLessonNotes[0][0]
            return SharingLessonNotes

    def delete_sharingLessonNotesAnnouncement_byId(id):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            statement = """DELETE FROM SHAREDLESSONNOTES WHERE SHAREDLESSONNOTES.ID = %s"""
            cursor.execute(statement, [id])