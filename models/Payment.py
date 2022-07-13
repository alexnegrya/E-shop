from db.templates import *


class Payment(Model):
    def __init__(self, id_, method, volume):
        self.id = id_
        self.inDB = False
        self.method = method
        self.volume = volume

    def __str__(self):
        title = f"--- Payment ---"
        id = f"Id: {self.id}"
        inDB = f'In DB: {self.inDB}'
        method = f'Method: {self.method}'
        volume = f'Volume: {self.volume}'
        return f'\n\n{title}\n{id}\n{inDB}\n{method}\n{volume}\n\n'

    def __repr__(self): return f'<<{[self.id, self.inDB, self.method, self.volume]}>>'

    def __setattr__(self, name, value):
        if name == 'id':
            if self.inDB == False:
                if type(value) != int:
                    raise TypeError('id must have an int value')
        elif name == 'inDB':
            if value not in (True, False):
                raise TypeError(
                    'value for inDB attribute must be True or False only')
        elif name == 'method':
            if type(value) != str:
                raise TypeError('method must be str type')
        elif name == 'volume':
            from .Money import Money
            if type(value) != Money:
                raise TypeError('volume must be Money type')
        object.__setattr__(self, name, value)

    def __eq__(self, other): return self.id == other.id if type(other) == Payment else False


class PaymentRepositoryFactory(ModelRepositoryFactory):
    def __init__(self, pgds): self.pgds = pgds

    def __str__(self):
        data = self.pgds.query('SELECT * FROM payments')
        if len(data) != 0:
            from .Money import MoneyRepositoryFactory
            mrf = MoneyRepositoryFactory(self.pgds)
            payments = []
            for row in data:
                p = self.get_payment(row[0], row[1], mrf.find_by_id(row[2]))
                p.inDB = True
                payments.append(p)
            out = ''
            for payment in payments:
                out = out + str(payment)
        else:
            out = '\nNo payments here\n'
        return out

    def __repr__(self): return str(self.pgds.query('SELECT * FROM payments'))

    # ##### Factory methods #####
    def get_payment(self, id_, method, volume): return Payment(id_, method, volume)

    # ##### Repository methods #####
    def all(self):
        data = self.pgds.query('SELECT * FROM payments')
        if len(data) > 0:
            from .Money import MoneyRepositoryFactory
            mrf = MoneyRepositoryFactory(self.pgds)
            payments = []
            for row in data:
                p = self.get_payment(row[0], row[1], mrf.find_by_id(row[2]))
                p.inDB = True
                payments.append(p)
            return payments
        else:
            return []

    def save(self, payment):
        # Type verify
        if type(payment) != Payment:
            raise TypeError('the entity should be only Payment type')
        # Save object data
        if payment.inDB == False:
            payment.id = self.pgds.query(f'INSERT INTO payments(method, price_id)\
                VALUES (\'{payment.method}\', {payment.volume.id})\
                RETURNING id')[0][0]
            payment.inDB = True
        elif payment.inDB:
            self.pgds.query(f'UPDATE payments\
                SET method = \'{payment.method}\', price_id = {payment.volume.id}, \
                WHERE id = {payment.id}')

    def save_many(self, *payments):
        # Checking object quantity
        l = len(payments)
        if l in [0, 1]:
            raise ValueError(f'at least 2 objects can be saved, not {l}')
        # Checking objects type
        for i in range(len(payments)):
            if type(payments[i]) != Payment:
                raise TypeError(f'object number {i+1} is not a Payment type')
        # Save objects data
        for payment in payments:
            if payment.inDB == False:
                payment.id = self.pgds.query(f'INSERT INTO payments(method, price_id)\
                    VALUES (\'{payment.method}\', {payment.volume.id})\
                    RETURNING id')[0][0]
                payment.inDB = True
            elif payment.inDB:
                self.pgds.query(f'UPDATE payments\
                    SET method = \'{payment.method}\', price_id = {payment.volume.id}, \
                    WHERE id = {payment.id}')

    def find_by_id(self, id_):
        # Checking type
        if type(id_) != int:
            raise TypeError('id must be int type')
        # search and remove
        data = self.pgds.query(f'SELECT * FROM payments WHERE id = {id_}')
        if len(data) > 0:
            from .Money import MoneyRepositoryFactory
            mrf = MoneyRepositoryFactory(self.pgds)
            p = self.get_payment(data[0][0], data[0][1], mrf.find_by_id(data[0][2]))
            p.inDB = True
            return p

    def delete_by_id(self, id_):
        # Checking type
        if type(id_) != int:
            raise TypeError('id must be int type')
        # Delete data
        self.pgds.query(f'DELETE FROM payments WHERE id = {id_}')
