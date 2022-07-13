from db.templates import *


class OrderItem(Model):
    def __init__(self, id_, quantity, product_id, order_id):
        self.id = id_
        self.inDB = False
        self.quantity = quantity
        self.product_id = product_id
        self.order_id = order_id

    def __str__(self):
        title = f"--- OrderItem ---"
        id = f"Id: {self.id}"
        inDB = f'In DB: {self.inDB}'
        quantity = f'Quantity: {self.quantity}'
        product_id = f'Product id: {self.product_id}'
        order_id = f'Order id: {self.order_id}'
        return f'\n\n{title}\n{id}\n{inDB}\n{quantity}\n{product_id}\n{order_id}\n\n'

    def __repr__(self):
        return f'<<{[self.id, self.inDB, self.quantity, self.product_id, self.order_id]}>>'

    def __setattr__(self, name, value):
        if name == 'id':
            if self.inDB == False:
                if type(value) != int: raise TypeError('id must have an int value')
        elif name == 'inDB':
            if type(value) != bool: raise TypeError('value for inDB attribute must be True or False only')
        elif name in ('quantity', 'product_id', 'order_id'):
            if type(value) != int: raise TypeError(f'{" ".join(name.split("_").strip())} must have integer value')
        object.__setattr__(self, name, value)

    def __eq__(self, other): return self.id == other.id if type(other) == OrderItem else False


class OrderItemRepositoryFactory(ModelRepositoryFactory):
    def __init__(self, pgds): self.pgds = pgds

    def __str__(self):
        data = self.pgds.query('SELECT * FROM order_items')
        if len(data) != 0:
            orderItems = []
            for row in data:
                oi = self.get_order_item(row[0], row[1], row[2])
                oi.inDB = True
                orderItems.append(oi)
            out = ''
            for orderItem in orderItems:
                out = out + str(orderItem)
        else:
            out = '\nNo order items here\n'
        return out

    def __repr__(self):
        return str(self.pgds.query('SELECT * FROM order_items'))

    # ##### Factory methods #####
    def get_order_item(self, id_, quantity, product_id, order_id):
        return OrderItem(id_, quantity, product_id, order_id)

    # ##### Repository methods #####
    def all(self):
        res = self.pgds.query('SELECT * FROM order_items')
        order_items = []
        for row in res:
            oi = self.get_order_item(row[0], row[1], row[2], row[3])
            oi.inDB = True
            order_items.append(oi)
        return order_items

    def save(self, order_item: OrderItem):
        if type(order_item) != OrderItem: raise TypeError('the entity should be only OrderItem type')
        if order_item.inDB == False:
            order_item.id = self.pgds.query(f'INSERT INTO order_items(quantity, product_id, order_id)\
                VALUES ({order_item.quantity}, {order_item.product_id}, {order_item.order_id})\
                RETURNING id')[0][0]
            order_item.inDB = True
        elif order_item.inDB:
            self.pgds.query(f'UPDATE order_items\
                SET quantity = {order_item.quantity}, product_id = {order_item.product_id}, order_id = {order_item.order_id}\
                WHERE id = {order_item.id}')

    def save_many(self, *order_items):
        # Checking object quantity
        l = len(order_items)
        if l in [0, 1]: raise ValueError(f'at least 2 objects can be saved, not {l}')
        # Checking objects type
        for i in range(l):
            if type(order_items[i]) != OrderItem: raise TypeError(f'object number {i+1} is not a OrderItem type')
        # Save objects data
        [self.save(order_item) for order_item in order_items]

    def find_by_id(self, id_):
        if type(id_) != int: raise TypeError('id must be int type')
        # Search and return
        try:
            data = self.pgds.query(f'SELECT * FROM order_items WHERE id = {id_}')[0]
            if len(data) > 0:
                oi = self.get_order_item(data[0], data[1], data[2], data[3])
                oi.inDB = True
                return oi
        except IndexError:
            pass

    def find_by_order_id(self, order_id: int) -> list[OrderItem]:
        if type(order_id) != int: raise ValueError('order id must be a integer value')
        return [self.get_order_item(row[0], row[1], row[2], row[3]) for row in \
            self.pgds.query(f'SELECT * FROM order_items WHERE order_id = {order_id}')]

    def delete_by_id(self, id_):
        if type(id_) != int: raise TypeError('id must be int value')
        self.pgds.query(f'DELETE FROM order_items WHERE id = {id_}')
