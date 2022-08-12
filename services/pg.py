import psycopg2
import re
from psycopg2.errors import InFailedSqlTransaction
from datetime import datetime


class PostgresDataService:
    def __init__(self, host, database, login, password):
        self.host = host
        self.database = database
        self.login = login
        self.password = password
    
    def open(self) -> None:
        self.conn = psycopg2.connect(
            host=self.host,
            dbname=self.database,
            user=self.login,
            password=self.password
        )
        
    def __format_value_for_query(self, value) -> str:
        value = str(value) if type(value) not in (str, datetime) else "'" + str(value).replace("'", "''") + "'"
        return value if value != 'None' else 'null'

    def __format_alias(self, value: str) -> str:
        spl = value.split('|')
        return f'{spl[0]} AS {spl[1]}' if len(spl) == 2 else value

    def __format_keyword(self, name: str, kwd) -> str:
        if name == 'where':
            if type(kwd) == str: return f' WHERE {kwd}'
            elif type(kwd) == dict and all([type(k) == str for k in kwd.keys()]):
                return f" WHERE {' AND '.join([f'{field} = {self.__format_value_for_query(value)}' for field, value in kwd.items()])}"
            else: return ''
        elif name == 'join':
            if type(kwd) == str:
                with kwd.split(" ON ") as spl: return f' JOIN {self.__format_alias(spl[0])} ON {spl[1]} ' if len(spl) == 2 else ''
            else: return ''
        elif name == 'returning':
            if type(kwd) != tuple: raise TypeError('returning kwd must be a tuple')
            elif any([type(v) != str for v in kwd]): raise ValueError('returning kwd tuple must contains str fields')
            else: return f' RETURNING {", ".join([self.__format_alias(rv) for rv in kwd])}'
        else: raise ValueError('unknown keyword')
    
    def query(self, query: str) -> list[tuple]:
        q = query.lower()
        while True:
            try:
                cursor = self.conn.cursor()
                if len(re.findall(r';(\s*[a-zA-Z]+\s+)', query)) <= 1: cursor.execute(query)
                else: cursor.executemany(query)
            except InFailedSqlTransaction:
                self.conn.rollback()
                continue
            self.conn.commit()
            return cursor.fetchall() if q.startswith('select') or 'returning' in q else []

    def insert(self, into_table: str, *returning, **values) -> list[tuple]:
        values = {k: self.__format_value_for_query(v) for k, v in values.items()}
        return self.query(f"INSERT INTO {into_table}({', '.join(values.keys())})\
 VALUES ({', '.join([str(value) for value in values.values()])}){self.__format_keyword('returning', returning)};")

    def update(self, table: str, where=None, **values) -> None:
        values = ', '.join([f'{k} = {self.__format_value_for_query(v)}' for k, v in values.items()])
        self.query(f"UPDATE {table} SET {values}{self.__format_keyword('where', where)};")

    def select(self, *fields: tuple[str], from_table: str, join=None, where=None) -> list[dict]:
        data = self.query(f"SELECT {', '.join(fields)} FROM {self.__format_alias(from_table)}\
{''.join([self.__format_keyword(name, kwd) for name, kwd in (('where', where), ('join', join))])}")
        return [{fields[i]: v for i, v in enumerate(row)} for row in data]

    def delete(self, from_table: str, where=None) -> None: self.query(f"DELETE FROM {from_table}{self.__format_keyword('where', where)}")
