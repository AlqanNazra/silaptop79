from django.db import connection

class BaseRepository:
    def execute (self, query, params = None, fetch_one=False, fetch_all = False):
        with connection.cursor() as cursor:
            cursor.execute(query, params or [])

            if fetch_one:
                return cursor.fetchone()

            if fetch_all:
                return cursor.fetchall()

            return None