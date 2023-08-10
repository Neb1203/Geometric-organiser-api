from controllers.DBConnect import DBConnect
from fastapi import FastAPI
from controllers.hashSalt import hashSalt
import secrets
import requests
from datetime import datetime, timedelta
class Authenticate:
    app = FastAPI()
    db_connect = DBConnect()

    def index(self, email, password):
        print("running", email, password)
        qry = """
                    SELECT ID
                    FROM playerDetails pd
                    WHERE pd.email = %s AND pd.password = %s
                    LIMIT 1
                """

        hashPassword = hashSalt(password)
        data = (email, hashPassword)

        self.db_connect.cursor.execute(qry, data)
        self.db_connect.cursor.reset()

        record = self.db_connect.cursor.fetchone()
        if record != None:
            token = secrets.token_urlsafe(24)

            qry = "INSERT INTO session (loginDate, sessionToken) VALUES (%s, %s)"
            data = (datetime.now(), token)

            self.db_connect.cursor.execute(qry, data)
            self.db_connect.cnx.commit()

            self.db_connect.cursor.reset()
            with open("tokens.txt", "a") as file:
                file.write(token + "\n")
            return token
        else:
            return "Account doesn't exist"


        # if (record == None) {
        # }
        # if not logged in then return status code of 422

        # if logd in add a new record to session table
    def validate(self, sessionToken):
        qry = """
            SELECT loginDate
            FROM session
            WHERE sessionToken = %s
            LIMIT 1
        """
        self.db_connect.cursor.execute(qry, (sessionToken,))
        self.db_connect.cursor.reset()
        record = self.db_connect.cursor.fetchone()
        print("validate", record)
        print(record)
        return record

