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

    def delete_sharingLessonNotesAnnouncement_byId(id):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            statement = """DELETE FROM SHAREDLESSONNOTES WHERE SHAREDLESSONNOTES.ID = %s"""
            cursor.execute(statement, [id])