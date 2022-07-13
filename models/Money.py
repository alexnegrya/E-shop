from db.templates import *


class Money(Model):
    def __init__(self, id_, amount, currency_char_code):
        self.id = id_
        self.inDB = False
        self.amount = amount
        self.currency_char_code = currency_char_code

    def __str__(self):
        title = f"--- Money ---"
        id_ = f'Id: {self.id}'
        inDB = f'In DB: {self.inDB}'
        amount = f'Amount: {self.amount}'
        currency_char_code = f'Currency: {self.currency_char_code}'
        out = f'\n\n{title}\n{id_}\n{inDB}\n{amount}\n{currency_char_code}\n\n'
        return out

    def __repr__(self):
        return f'<<{[self.id, self.inDB, self.amount, self.currency_char_code]}>>'

    def __setattr__(self, name, value):
        if name == 'id':
            if self.inDB == False:
                if type(value) != int:
                    raise TypeError('id must have an int value')
        elif name == 'inDB':
            if value not in (True, False):
                raise TypeError('value for inDB attribute must be True or False only')
        elif name == 'amount':
            if type(value) not in (int, float): raise TypeError('amount must be int or float type')
        elif name == 'currency_char_code':
            if type(value) != str: raise TypeError('wrong currency_char_code type, it must be only str')
        object.__setattr__(self, name, value)

    def __eq__(self, other): return self.id == other.id if type(other) == Money else False


class MoneyRepositoryFactory(ModelRepositoryFactory):
    def __init__(self, pgds):
        self.pgds = pgds

    def __str__(self):
        data = self.pgds.query('SELECT * FROM money')
        if len(data) != 0:
            money = []
            for row in data:
                m = self.get_money(row[0], row[1], row[2])
                m.inDB = True
                money.append(m)
            out = ''
            for obj in money:
                out = out + str(obj)
        else:
            out = '\nNo money here\n'
        return out

    def __repr__(self):
        return str(self.pgds.query('SELECT * FROM money'))

    # ##### Factory methods #####
    def get_money(self, id_, amount, currency_char_code):
        return Money(id_, amount, currency_char_code)

    # ##### Repository methods #####
    def all(self):
        res = self.pgds.query('SELECT * FROM money')
        if len(res) > 0:
            money = []
            for row in res:
                m = self.get_money(row[0], row[1], row[2])
                m.inDB = True
                money.append(m)
            return money
        else:
            return []

    def save(self, money):
        # Type verify
        if type(money) != Money:
            raise TypeError('the entity should be only Money type')
        # Save object data
        if money.inDB == False:
            money.id = self.pgds.query(f'INSERT INTO money(amount, currency_char_code)\
                VALUES ({money.amount}, \'{money.currency_char_code}\') RETURNING id')[0][0]
            money.inDB = True
        elif money.inDB:
            self.pgds.query(f'UPDATE money\
                SET amount = {money.amount}, currency_char_code = \'{money.currency_char_code}\'\
                WHERE id = {money.id}')

    def save_many(self, *money):
        # Checking object quantity
        l = len(money)
        if l in [0, 1]: raise ValueError(f'at least 2 objects can be saved, not {l}')
        # Checking objects type
        for i in range(l):
            if type(money[i]) != Money: raise TypeError(f'object number {i+1} is not a Money type')
        # Save objects data
        [self.save(m) for m in money]

    def find_by_id(self, id_):
        # Checking type
        if type(id_) != int: raise TypeError('id must be int type')
        # Search and return
        data = self.pgds.query(f'SELECT * FROM money WHERE id = {id_}')
        if len(data) != 0:
            money = self.get_money(data[0][0], data[0][1], data[0][2])
            money.inDB = True
            return money

    def delete_by_id(self, id_):
        # Checking type
        if type(id_) != int:
            raise TypeError('id must be int type')
        # Delete data
        self.pgds.query(f'DELETE FROM money WHERE id = {id_}')
