import time

from fastapi import FastAPI

from controllers.DBConnect import DBConnect
from controllers.session import PlayerDetails


class GameSaves:
    app = FastAPI()
    db_connect = DBConnect()
    session = PlayerDetails()

    def store(self, mode: str, score: int, session: str, duration: time, campaignLevel):
        playerId = self.session.getPlayerId(session)
        if playerId == None:
            return

        qry = """
            INSERT INTO gamesaves (mode, score, fkPlayerId, duration)
            VALUES (%s, %s, %s, %s)
        """
        data = [mode, score, playerId, duration]

        if mode == "CAMPAIGN":
            qry = """
                    INSERT INTO gamesaves (mode, score, fkPlayerId, duration, campaignLevel)
                    VALUES (%s, %s, %s, %s, %s)
                """
            data = [mode, score, playerId, duration, campaignLevel]
        self.db_connect.cursor.execute(qry, data)

        self.db_connect.cnx.commit()
        self.db_connect.cursor.reset()

    def get(self, session: str):
        playerId = self.session.getPlayerId(session)
        if playerId == None:
            return

        qry = """
            SELECT JSON_ARRAY(
                JSON_OBJECT(
                    'ID', ID,
                    'campaignLevel', campaignLevel,
                    'mode', mode,
                    'score', score,
                    'duration', duration,
                    'fkPlayerId', fkPlayerId
                )
            ) FROM gamesaves
            WHERE fkPlayerId = %s
        """
        data = [playerId]
        self.db_connect.cursor.execute(qry, data)
        gameSaves = self.db_connect.cursor.fetchall()
        self.db_connect.cursor.reset()
        return gameSaves

