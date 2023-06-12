import secrets

from fastapi import FastAPI
from controllers.DBConnect import DBConnect
from controllers.hashSalt import hashSalt
class PlayerDetails:
    app = FastAPI()
    db_connect = DBConnect()
        # hashSalt = hashSalt()

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
        hexHash = hashSalt(password)
        token = secrets.token_urlsafe(48)

        qry = "INSERT INTO playerDetails (token, userName, password, email) VALUES (%s, %s, %s, %s)"
        data = (token, user_name, hexHash, email)

        self.db_connect.cursor.execute(qry, data)
        self.db_connect.cnx.commit()

        self.db_connect.cursor.reset()
        return "success"
