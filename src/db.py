import mysql.connector
from mysql.connector.pooling import MySQLConnectionPool
from dotenv import load_dotenv
import os


class Database:
    def __init__(self):
        load_dotenv()
        self.pool = MySQLConnectionPool(
            pool_name="flight_pool",
            pool_size=5,
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASS"),
            database="flight_game"
        )

    def get_conn(self):
        return self.pool.get_connection()

    def query_all(self, sql: str, params=None):
        conn = self.get_conn()
        try:
            with conn.cursor(buffered=True) as cursor:
                cursor.execute(sql, params or ())
                return cursor.fetchall()
        finally:
            conn.close()

    def execute(self, sql: str, params=None):
        conn = self.get_conn()
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, params or ())
            conn.commit()
        finally:
            conn.close()