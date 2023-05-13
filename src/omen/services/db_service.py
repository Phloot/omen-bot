import os

import psycopg
from psycopg.rows import class_row

from models.user import User

# Be sure to use parameterized queries and not f strings to pass arguments
# Failing to do so could lead to SQL injection attacks
class DbService:

    def __init__(self):
        self.connection = psycopg.connect(
            dbname="co_db",
            host="db",
            port=5432,
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASSWORD'])
        self.cursor = self.connection.cursor

    def __del__(self):
        self.connection.close()

    def get_all_users(self):
        cur = self.cursor(row_factory=class_row(User))
        res = cur.execute("SELECT * FROM coguild.users").fetchall()
        return res

    def insert_user(self, discord_id, api_key: None, gw2_account_id: None, gw2_account_name: None):
        cur = self.cursor()
        res = cur.execute("INSERT INTO coguild.users (discord_id, api_key, gw2_account_id, gw2_account_name) "
                          "VALUES (%s, %s, %s, %s) "
                          "ON CONFLICT (discord_id) DO UPDATE SET "
                          "gw2_account_name = EXCLUDED.gw2_account_name, "
                          "api_key = COALESCE(EXCLUDED.api_key, coguild.users.api_key), "
                          "gw2_account_id = COALESCE(EXCLUDED.gw2_account_id, coguild.users.gw2_account_id)",
                          (discord_id, api_key, gw2_account_id, gw2_account_name))
        self.connection.commit()
        return res

    def delete_user_api_key(self, discord_id):
        cur = self.cursor()
        res = cur.execute("DELETE FROM coguild.users WHERE discord_id = %s", (str(discord_id),))
        self.connection.commit()
        return res
