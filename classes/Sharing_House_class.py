from flask import current_app
from flask_login import UserMixin
import psycopg2 as dbapi2

class sharingHouseAnnouncement:
    def __init__(self,location,rentPrice,numberOfPeople,numberOfRoom,description,currentuser_id):
        self.LocationOfSharingHouse = location
        self.RentPriceOfSharingHouse = rentPrice
        self.NumberOfPeopleInSharingHouse = numberOfPeople
        self.NumberOfSharingHouseRoom = numberOfRoom
        self.DescriptionOfSharingHouse  = description
        self.id_ownerOfSharingHouseAnnouncement = currentuser_id

    def get_LocationOfSharingHouse(self):
        return self.LocationOfSharingHouse
    def get_RentPriceOfSharingHouse(self):
        return self.RentPriceOfSharingHouse
    def get_NumberOfPeopleInSharingHouse(self):
        return self.NumberOfPeopleInSharingHouse
    def get_NumberOfSharingHouseRoom(self):
        return self.NumberOfSharingHouseRoom
    def get_DescriptionOfSharingHouse(self):
        return self.DescriptionOfSharingHouse
    def get_id_ownerOfSharingHouseAnnouncement(self):
        return self.id_ownerOfSharingHouseAnnouncement
    def get_id(self):
        return self.id

    def get_sharingHouseAnnouncement_byId(id):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            statement = """SELECT * FROM DATASHAREDHOUSE WHERE DATASHAREDHOUSE.ID = %s"""
            cursor.execute(statement, [id])
            db_SharingHouse = cursor.fetchall()
            SharingHouse = sharingHouseAnnouncement(db_SharingHouse[0][1], db_SharingHouse[0][2], db_SharingHouse[0][3], db_SharingHouse[0][4], db_SharingHouse[0][5],db_SharingHouse[0][6])
            SharingHouse.id = db_SharingHouse[0][0]
            return SharingHouse

    def delete_sharingHouseAnnouncement_byId(id):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            statement = """DELETE FROM DATASHAREDHOUSE WHERE DATASHAREDHOUSE.ID = %s"""
            cursor.execute(statement, [id])
