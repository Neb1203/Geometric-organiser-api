import secrets
from helpers.tokenModifier import TokenModifier
from fastapi import FastAPI
from controllers.DBConnect import DBConnect
from controllers.hashSalt import hashSalt
TokenModifier = TokenModifier()

class Login:
    app = FastAPI()
    db_connect = DBConnect()
    def username(self):
        qry = """
                    SELECT
                    pd.userName
                    FROM
                    session ss
                    LEFT JOIN playerdetails pd on pd._fk_session = ss.ID
                    WHERE
                    ss.ID in %s
                """
        sessionTokens = TokenModifier.read_session_ids()
        self.db_connect.cursor.execute(qry, (sessionTokens,))
        self.db_connect.cursor.reset()
        record = self.db_connect.cursor.fetchone()
        print("validate", record)
        print(record)
        return record
    def write(self, user_name, email, password):
        hexHash = hashSalt(password)
        token = secrets.token_urlsafe(48)

        qry = "INSERT INTO playerDetails (token, userName, password, email) VALUES (%s, %s, %s, %s)"
        data = (token, user_name, hexHash, email)

        self.db_connect.cursor.execute(qry, data)
        self.db_connect.cnx.commit()

        self.db_connect.cursor.reset()
