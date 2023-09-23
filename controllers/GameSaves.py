import time

from fastapi import FastAPI

from controllers.DBConnect import DBConnect
from controllers.session import PlayerDetails


class GameSaves:
    app = FastAPI()
    db_connect = DBConnect()
    session = PlayerDetails()

    def store(self, mode: str, score: int, session: str, duration: time, campaignLevel, campaignWinOrLoss):
        playerDetails = self.session.readSession(session)
        if len(playerDetails) == 0:
            return

        playerId = playerDetails[3]
        qry = """
            INSERT INTO gamesaves (mode, score, fkPlayerId, duration)
            VALUES (%s, %s, %s, %s)
        """
        data = [mode, score, playerId, duration]

        if mode == "CAMPAIGN":
            qry = """
                    INSERT INTO gamesaves (mode, score, fkPlayerId, duration, campaignLevel, campaignWinOrloss)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
            data = [mode, score, playerId, duration, campaignLevel, campaignWinOrLoss]
        self.db_connect.cursor.execute(qry, data)

        self.db_connect.cnx.commit()
        self.db_connect.cursor.reset()

