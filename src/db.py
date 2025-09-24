import mysql.connector
from dotenv import load_dotenv
import os

class DatabaseMeta:
    def __init__(self):
        self.host: str = os.getenv("MYSQL_HOST")
        self.user: str = os.getenv("MYSQL_USER")
        self.password: str = os.getenv("MYSQL_PASS")

class Database:
    def __init__(self):
        load_dotenv()
        self.meta: DatabaseMeta = DatabaseMeta()
        self.conn = None


    def connect(self):
        conn = mysql.connector.connect(
            host=self.meta.host,
            user=self.meta.user,
            password=self.meta.password,
            database="flight_game"
        )
        self.conn = conn
    
    def disconnect(self):
        self.conn.close()
        self.conn = None

    def query(self, sql: str):
        cur = self.conn.cursor()
        cur.execute(sql)
        res = cur.fetchall()
        return res