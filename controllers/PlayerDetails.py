from fastapi import FastAPI
from controllers.DBConnect import DBConnect
import hashlib
from dotenv import load_dotenv
import os
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
        salt = b']:\xfb+\x9e\xa8\x9e4\x16\x0eo\x0f;\xd5\xee\xed%\xc7\xe9\xcc/\xeb|J\xed\xcc\xdf\xe7\x01\x01\xcb\xf9'
        passwordHash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 10000)
        hexHash = passwordHash.hex()

        qry = "INSERT INTO playerDetails (userName, password, email) VALUES (%s, %s, %s)"
        data = (user_name, hexHash, email)

        self.db_connect.cursor.execute(qry, data)
        self.db_connect.cnx.commit()

        self.db_connect.cursor.reset()
        return "success"
