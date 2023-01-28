import os

import psycopg
from psycopg.rows import class_row

from src.omen.models.user import User


class DbService:

    def __new__(cls):
        connection = psycopg.connect(
            dbname="postgres",
            host="localhost",
            port=5432,
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASSWORD'])
        cls.cursor = connection.cursor
        return object.__new__(cls)
    async def test(self):
        res = self.cursor("select * from coguild.users")
        return len(res)

    def get_all_users(self):
        cur = self.cursor(row_factory=class_row(User))
        res = cur.execute("select * from coguild.users").fetchall()
        return res

