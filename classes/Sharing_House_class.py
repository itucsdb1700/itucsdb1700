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

    def delete_sharingHouseAnnouncement_byId(id):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            statement = """DELETE FROM DATASHAREDHOUSE WHERE DATASHAREDHOUSE.ID = %s"""
            cursor.execute(statement, [id])
