from fastapi import FastAPI
from controllers.DBConnect import DBConnect

class PlayerDetails:
    app = FastAPI()
    db_connect = DBConnect()

    def write(self, user_name, email, password):
        qry = "INSERT INTO playerDetails (userName, password, email) VALUES (%s, %s, %s)"
        data = (user_name, password, email)

        self.db_connect.cursor.execute(qry, data)
        self.db_connect.cnx.commit()

        self.db_connect.cursor.close()
        self.db_connect.cnx.close()
        return "success"
