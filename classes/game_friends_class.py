from flask import current_app
from flask_login import UserMixin
import psycopg2 as dbapi2

class GameAnnounce:
    def __init__(self, gameName, gameType, playerNum, gameDate, gameLoc, gameDesc, user_id):
        self.gameName = gameName
        self.gameType = gameType
        self.playerNum = playerNum
        self.gameDate = gameDate
        self.gameLoc = gameLoc
        self.gameDesc = gameDesc
        self.user_id = user_id

    def get_gameName(self):
        return self.gameName
    def get_gameType(self):
        return self.gameType
    def get_playerNum(self):
        return self.playerNum
    def get_gameDate(self):
        return self.gameDate
    def get_gameLoc(self):
        return self.gameLoc
    def get_gameDesc(self):
        return self.gameDesc
    def get_user_id(self):
        return self.user_id
    def get_id(self):
        return self.id


    def get_announce_byId(announceId):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            statement = """SELECT * FROM GAMEFRIEND WHERE GAMEFRIEND.ID = %s"""
            cursor.execute(statement, [announceId])
            db_announce = cursor.fetchall()
            announce = GameAnnounce(db_announce[0][1], db_announce[0][2], db_announce[0][5], db_announce[0][3], db_announce[0][4], db_announce[0][6], db_announce[0][7])
            announce.id = db_announce[0][0]
            return announce

    def delete_announce_byId(announceId):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            statement = """DELETE FROM GAMEFRIEND WHERE GAMEFRIEND.ID = %s"""
            cursor.execute(statement, [announceId])


