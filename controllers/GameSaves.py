from fastapi import FastAPI

from controllers.DBConnect import DBConnect


class GameSaves:
    app = FastAPI()
    db_connect = DBConnect()
    def store(self, mode: str, score: int, session: str, campaignLevel, campaignWinOrLoss):
        qry = """
            INSERT INTO gamesaves (mode, score, fkSession)
            VALUES (%s, %s, %s)
        """
        data = [mode, score, session]

        if mode == "CAMPAIGN":
            qry = """
                    INSERT INTO gamesaves (mode, gameScore, fkSession, campaignLevel, campaignWinOrloss)
                    VALUES (%s, %s, %s, %s, %s)
                """
            data = [mode, score, session, campaignLevel, campaignWinOrLoss]
        self.db_connect.cursor.execute(qry, data)

        self.db_connect.cnx.commit()
        self.db_connect.cursor.reset()