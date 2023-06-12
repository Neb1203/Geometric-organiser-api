import secrets
import json
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
            'token', token,
            'username', userName,
            'password', password,
            'email', email
        ) FROM playerDetails
        WHERE email=%s AND password = %s
        LIMIT 1"""
        hashPassword = hashSalt(password)
        data = (email, hashPassword)

        self.db_connect.cursor.execute(qry, data)
        self.db_connect.cursor.reset()

        row = self.db_connect.cursor.fetchone()  # Fetch the first row

        if row is not None:
            json_object = row[0]  # Retrieve the JSON object as a string
            parsed_json = json.loads(json_object)  # Parse the JSON string into a Python object

            self.user_name_value = parsed_json['username']  # Access the value of the 'token' key
            return self.user_name_value
        else:
            return None
    def write(self, user_name, email, password):
        hexHash = hashSalt(password)
        token = secrets.token_urlsafe(48)

        qry = "INSERT INTO playerDetails (token, userName, password, email) VALUES (%s, %s, %s, %s)"
        data = (token, user_name, hexHash, email)

        self.db_connect.cursor.execute(qry, data)
        self.db_connect.cnx.commit()

        self.db_connect.cursor.reset()
        return "success"
