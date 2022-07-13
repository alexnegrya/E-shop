import psycopg2
import re


class PGDataService:
    def __init__(self, host, database, login, pass_):
        self.host = host
        self.database = database
        self.login = login
        self.password = pass_
    
    def open(self):
        self.conn = psycopg2.connect(
            host=self.host,
            dbname=self.database,
            user=self.login,
            password=self.password
        )
    
    def format_query_string(query: str):
        return query.replace('None', 'null')
    
    def query(self, query: str):
        cursor = self.conn.cursor()
        query = self.format_query_string(query)
        if len(re.findall(';', query)) <= 1: cursor.execute(query)
        else: cursor.executemany(query)
        self.conn.commit()
        q = query.lower()
        return cursor.fetchall() if q.startswith('select') or 'returning' in q else []
