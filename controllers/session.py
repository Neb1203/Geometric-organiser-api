from fastapi import FastAPI
from controllers.DBConnect import DBConnect


class PlayerDetails:
    app = FastAPI()
    db_connect = DBConnect()

    def read(self, email, password):
        qry = """SELECT JSON_OBJECT(
            'id', id,
            'email', email,
            'user_id', userId,
            'username', userName,
            'password', password,
            'email', email
        ) FROM playerDetails
        WHERE email=%s AND password = %s
        LIMIT 1"""
        data = (email, password)

        self.db_connect.cursor.execute(qry, data)
        json_result = self.db_connect.cursor.fetchall()
        self.db_connect.cursor.reset()
        return json_result

    def write(self, user_name, email, password):
        qry = "INSERT INTO playerDetails (userName, password, email) VALUES (%s, %s, %s)"
        data = (user_name, password, email)

        self.db_connect.cursor.execute(qry, data)
        self.db_connect.cnx.commit()

        self.db_connect.cursor.close()
        self.db_connect.cnx.close()
        return "success"

    def readSession(self, session: str) -> tuple:
        qry = """SELECT * FROM session
                WHERE sessionToken=%s
                LIMIT 1"""
        data = [session]

        self.db_connect.cursor.execute(qry, data)
        result = self.db_connect.cursor.fetchone()
        self.db_connect.cursor.reset()
        return result

    def getPlayerId(self, session: str):
        playerDetails = self.readSession(session)
        if len(playerDetails) == 0:
            return None

        return playerDetails[3]
