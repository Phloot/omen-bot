import os

import psycopg
from psycopg.rows import class_row

from src.omen.models.user import User


class DbService:

    def __new__(cls):
        cls.connection = psycopg.connect(
            dbname="postgres",
            host="localhost",
            port=5432,
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASSWORD'])
        cls.cursor = cls.connection.cursor
        return object.__new__(cls)

    def get_all_users(self):
        cur = self.cursor(row_factory=class_row(User))
        res = cur.execute("select * from coguild.users").fetchall()
        return res

    def insert_user(self, discord_id, api_key):
        cur = self.cursor()
        res = cur.execute("insert into coguild.users(discord_id, api_key) "
                          "VALUES (%s, %s)"
                          "ON CONFLICT DO NOTHING ", (discord_id, api_key))
        self.connection.commit()
        return res

    def delete_user_api_key(self, discord_id):
        cur = self.cursor()
        res = cur.execute("delete from coguild.users where discord_id = %s", [str(discord_id)])
        self.connection.commit()
        return res
