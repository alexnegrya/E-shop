import psycopg2
import re


class PostgresORM:
    def __init__(self, host, database, login, password):
        self.host = host
        self.database = database
        self.login = login
        self.password = password
    
    def open(self):
        self.conn = psycopg2.connect(
            host=self.host,
            dbname=self.database,
            user=self.login,
            password=self.password
        )
        
    def format_value_for_query(self, value):
        return value if type(value) != str else "'" + value.replace("'", "''") + "'" if value != None else 'null'

    def format_alias(self, value: str):
        spl = value.split('|')
        return f'{spl[0]} AS {spl[1]}' if len(spl) == 2 else value

    def format_keyword(self, name: str, kwd):
        if name == 'where': return f' WHERE {kwd}' if type(kwd) == str else ''
        elif name == 'join':
            if type(kwd) == str:
                with kwd.split(" ON ") as spl: return f' JOIN {self.format_alias(spl[0])} ON {spl[1]} ' if len(spl) == 2 else ''
            else: return ''
    
    def query(self, query: str):
        cursor = self.conn.cursor()
        if len(re.findall(';', query)) <= 1: cursor.execute(query)
        else: cursor.executemany(query)
        self.conn.commit()
        q = query.lower()
        return cursor.fetchall() if q.startswith('select') or 'returning' in q else []

    def insert(self, into_table: str, returning=None, **values):
        values = {k: self.format_value_for_query(v) for k, v in values.items()}
        returning = f' RETURNING {returning}' if type(returning) == str else ''
        data = self.query(f"INSERT INTO {into_table}({', '.join(values.keys())}) VALUES ({', '.join(values.values())}){returning};")
        if data != None: return data

    def update(self, table: str, where=None, **values):
        values = ', '.join([f'{k} = {v}' for k, v in values.items()])
        self.query(f"UPDATE {table} SET {values}{self.format_keyword('where', where)};")

    def select(self, *fields: tuple[str], from_table: str, join=None, where=None):
        self.query(f"SELECT {', '.join(fields)} FROM {self.format_alias(from_table)}\
            {''.join([self.format_keyword(name, kwd) for name, kwd in (('where', where), ('join', join))])}")

    def delete(self, from_table: str, where=None): self.query(f"DELETE FROM {from_table}{self.format_keyword('where', where)}")
