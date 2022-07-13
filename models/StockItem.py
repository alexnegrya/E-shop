from db.templates import *


class StockItem(Model):
    def __init__(self, id_, quantity, product_id):
        self.id = id_
        self.inDB = False
        self.quantity = quantity
        self.product_id = product_id

    def __str__(self):
        title = f"--- StockItem ---"
        id = f"Id: {self.id}"
        inDB = f'In DB: {self.inDB}'
        quantity = f'Quantity: {self.quantity}'
        product_id = f'Item id: {self.product_id}'
        return f'\n\n{title}\n{id}\n{inDB}\n{quantity}\n{product_id}\n\n'

    def __repr__(self):
        return f'<<{[self.id, self.inDB, self.quantity, self.product_id]}>>'

    def __setattr__(self, name, value):
        if name == 'id':
            if self.inDB == False:
                if type(value) != int: raise TypeError('id must have an int value')
        elif name == 'inDB':
            if value not in (True, False):
                raise TypeError(
                    'value for inDB attribute must be True or False only')
        elif name == ('quantity', 'product_id'):
            if type(value) != int:
                raise TypeError('wrong type of quantity/product_id attribute')
        object.__setattr__(self, name, value)

    def __eq__(self, other): return self.id == other.id if type(other) == StockItem else False


class StockItemRepositoryFactory(ModelRepositoryFactory):
    def __init__(self, pgds): self.pgds = pgds

    def __str__(self): return ''.join(self.all()) if len(self.all()) > 0 else '\nNo stock items here\n'

    def __repr__(self): return str(self.pgds.query('SELECT * FROM stock_items'))

    # ##### Factory methods #####
    def get_stock_item(self, id_, quantity, product_id): return StockItem(id_, quantity, product_id)

    # ##### Repository methods #####
    def all(self):
        stock_items = self.pgds.query('SELECT * FROM stock_items')
        if len(stock_items) != 0:
            sI = []
            for row in stock_items:
                si = self.get_stock_item(row[0], row[1], row[2])
                si.inDB = True
                sI.append(si)
            return sI
        else: return []

    def save(self, stock_item):
        if type(stock_item) != StockItem: raise TypeError('the entity should be only StockItem type')
        if any([si.id == stock_item.id for si in self.all()]): raise ValueError('StockItem product_id is not unique')
        # Save object data
        if stock_item.inDB == False:
            stock_item.id = self.pgds.query(f'INSERT INTO stock_items(quantity, product_id)\
                VALUES ({stock_item.quantity}, {stock_item.product_id})\
                RETURNING id')[0][0]
            stock_item.inDB = True
        elif stock_item.inDB:
            self.pgds.query(f'UPDATE stock_items\
                SET quantity = {stock_item.quantity}, product_id = {stock_item.product_id}, \
                WHERE id = {stock_item.id}')

    def save_many(self, *stock_items):
        # Checking object quantity
        l = len(stock_items)
        if l in [0, 1]: raise ValueError(f'at least 2 objects can be saved, not {l}')
        # Checking objects type
        for i in range(l):
            if type(stock_items[i]) != StockItem:
                raise TypeError(f'object number {i+1} is not a StockItem type')
        # Save objects data
        [self.save(stock_item) for stock_item in stock_items]

    def find_by_id(self, id_):
        if type(id_) != int: raise TypeError('id must be int')
        data = self.pgds.query(f'SELECT * FROM stock_items WHERE id = {id_}')
        if len(data) > 0:
            si = self.get_stock_item(data[0][0], data[0][1], data[0][2])
            si.inDB = True
            return si

    def delete_by_id(self, id_):
        if type(id_) != int: raise TypeError('id must be int')
        self.pgds.query(f'DELETE FROM stock_items WHERE id = {id_}')
