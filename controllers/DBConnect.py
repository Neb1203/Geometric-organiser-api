import mysql.connector

class DBConnect:
    cnx = mysql.connector.connect(host='127.0.0.1', port='3306', user='neb120', password='Bentofon12',
                                  database='geometricDatabase')
    cursor = cnx.cursor()