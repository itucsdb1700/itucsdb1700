from flask import current_app
from flask_login import UserMixin
import psycopg2 as dbapi2

class searchingHouseAnnouncement:
    def __init__(self,location,mixRent,maxRent,description,currentuser_id):
        self.LocationOfSearchingHouse = location
        self.MinRentPriceOfSearchingHouse = mixRent
        self.MaxRentPriceOfSearchingHouse = maxRent
        self.DescriptionOfSearchingHouse = description
        self.id_ownerOfSearchingHouseAnnouncement = currentuser_id

    def get_LocationOfSearchingHouse(self):
        return self.LocationOfSearchingHouse

    def get_MinRentPriceOfSearchingHouse(self):
        return self.MinRentPriceOfSearchingHouse

    def get_MaxRentPriceOfSearchingHouse(self):
        return self.MaxRentPriceOfSearchingHouse

    def get_DescriptionOfSearchingHouse(self):
        return self.DescriptionOfSearchingHouse

    def get_id_ownerOfSearchingHouseAnnouncement(self):
        return self.id_ownerOfSearchingHouseAnnouncement
    def get_id(self):
        return self.id



    def get_searchingHouseAnnouncement_byId(id):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            statement = """SELECT * FROM DATASEARCHEDHOUSE WHERE USERID = %s"""
            cursor.execute(statement, [id])
            db_searchingHouse = cursor.fetchall()
            SearchingHouse = searchingHouseAnnouncement(db_searchingHouse[0][1],db_searchingHouse[0][2],db_searchingHouse[0][3],db_searchingHouse[0][4],db_searchingHouse[0][5])
            SearchingHouse.id = db_searchingHouse[0][0]
            return SearchingHouse


    def delete_searchingHouseAnnouncement_byId(id):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            statement = """DELETE FROM DATASEARCHEDHOUSE WHERE DATASEARCHEDHOUSE.ID = %s"""
            cursor.execute(statement, [id])