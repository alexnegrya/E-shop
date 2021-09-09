class Money:
    def __init__(self, id_, amount, currencyCharCode):
        self.id = id_
        self.inDB = False
        self.amount = amount
        self.currencyCharCode = currencyCharCode

    def __str__(self):
        title = f"--- Money ---"
        id_ = f'Id: {self.id}'
        inDB = f'In DB: {self.inDB}'
        amount = f'Amount: {self.amount}'
        currencyCharCode = f'Currency: {self.currencyCharCode}'
        out = f'\n\n{title}\n{id_}\n{inDB}\n{amount}\n{currencyCharCode}\n\n'
        return out

    def __repr__(self):
        return f'<<{[self.id, self.inDB, self.amount, self.currencyCharCode]}>>'

    def __setattr__(self, name, value):
        if name == 'id':
            if self.inDB == False:
                if type(value) == int:
                    object.__setattr__(self, name, value)
                else:
                    raise TypeError('id must have an int value')
        elif name == 'inDB':
            if value in (True, False):
                object.__setattr__(self, name, value)
            else:
                raise TypeError('value for inDB attribute must be True or False only')
        elif name == 'amount':
            if type(value) not in (int, float):
                raise TypeError('amount must be int or float type')
            else:
                object.__setattr__(self, name, value)
        elif name == 'currencyCharCode':
            if type(value) != str:
                raise TypeError('wrong currencyCharCode type, it must be only str')
            else:
                object.__setattr__(self, name, value)
        else:
            object.__setattr__(self, name, value)

    def __eq__(self, other):
        if type(other) == Money:
            if self.id == other.id:
                return True
            else:
                return False


class MoneyRepositoryFactory:
    def __init__(self, pgds):
        self.pgds = pgds

    def __str__(self):
        data = self.pgds.query('SELECT * FROM money')
        if len(data) != 0:
            money = []
            for row in data:
                m = self.getMoney(row[0], row[1], row[2])
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
    def getMoney(self, id_, amount, currencyCharCode):
        return Money(id_, amount, currencyCharCode)

    # ##### Repository methods #####
    def all(self):
        res = self.pgds.query('SELECT * FROM money')
        if len(res) > 0:
            money = []
            for row in res:
                m = self.getMoney(row[0], row[1], row[2])
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
                VALUES ({money.amount}, \'{money.currencyCharCode}\') RETURNING id')[0][0]
            money.inDB = True
        elif money.inDB:
            self.pgds.query(f'UPDATE money\
                SET amount = {money.amount}, currency_char_code = \'{money.currencyCharCode}\'\
                WHERE id = {money.id}')

    def save_many(self, *money):
        # Checking object quantity
        l = len(money)
        if l in [0, 1]:
            raise ValueError(f'at least 2 objects can be saved, not {l}')
        # Checking objects type
        for i in range(len(money)):
            if type(money[i]) != Money:
                raise TypeError(f'object number {i+1} is not a Money type')
        # Save objects data
        for m in money:
            if m.inDB == False:
                m.id = self.pgds.query(f'INSERT INTO money(amount, currency_char_code)\
                    VALUES ({m.amount}, \'{m.currencyCharCode}\') RETURNING id')[0][0]
                m.inDB = True
            elif m.inDB:
                self.pgds.query(f'UPDATE money\
                    SET amount = {m.amount}, currency_char_code = \'{m.currencyCharCode}\'\
                    WHERE id = {m.id}')

    def findById(self, id_):
        # Checking type
        if type(id_) != int:
            raise TypeError('id must be int type')
        # Search and return
        data = self.pgds.query(f'SELECT * FROM money WHERE id = {id_}')
        if len(data) != 0:
            money = self.getMoney(data[0][0], data[0][1], data[0][2])
            money.inDB = True
            return money

    def deleteById(self, id_):
        # Checking type
        if type(id_) != int:
            raise TypeError('id must be int type')
        # Delete data
        self.pgds.query(f'DELETE FROM money WHERE id = {id_}')
