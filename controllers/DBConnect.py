import mysql.connector
from dotenv import load_dotenv
import os

class DBConnect:
    load_dotenv()

    cnx = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME")
    )
    cursor = cnx.cursor()