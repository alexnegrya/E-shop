import psycopg2

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
    
    def query(self, query):
        cursor = self.conn.cursor()
        cursor.execute(query)
        self.conn.commit()
        return cursor.fetchall()
