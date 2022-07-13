from db.templates import *


class Order(Model):
    def __init__(self, id_, items_list, total_cost, payment_id, customer_id):
        self.id = id_
        self.inDB = False
        self.items_list = items_list
        self.total_cost = total_cost
        self.payment_id = payment_id
        self.customer_id = customer_id

    def __str__(self):
        title = f"--- Order ---"
        id = f"Id: {self.id}"
        inDB = f'In DB: {self.inDB}'
        items_list = f'Item list: {self.items_list}'
        total_cost = f'Total cost: {self.total_cost}'
        payment_id = f'Payment id: {self.payment_id}'
        customer_id = f'Customer id: {self.customer_id}'
        out = f'\n\n{title}\n{id}\n{inDB}\n{items_list}\n{total_cost}\n{payment_id}\n{customer_id}\n\n'
        return out

    def __repr__(self):
        return f'<<{[self.id, self.inDB, self.items_list, self.total_cost, self.payment_id, self.customer_id]}>>'

    def __setattr__(self, name, value):
        if name == 'id':
            if self.inDB == False:
                if type(value) != int: raise TypeError('id must have an int value')
        elif name == 'inDB':
            if value not in (True, False):
                raise TypeError(
                    'value for inDB attribute must be True or False only')
        elif name == 'items_list':
            from .OrderItem import OrderItem
            if type(value) != list:
                raise TypeError('items_list must be list type')
            for v in value:
                if type(v) != OrderItem:
                    raise TypeError('items_list must be contain only OrderItem type objects')
        elif name == 'total_cost':
            from .Money import Money
            if type(value) != Money:
                raise TypeError('total_cost must be Money type')
        elif name == 'payment_id':
            if type(value) != int:
                raise TypeError('payment_id must be int type')
        elif name == 'customer_id':
            if type(value) != int:
                raise TypeError('customer_id must be int type')
        object.__setattr__(self, name, value)

    def __eq__(self, other): return self.id == other.id if type(other) == Order else False


class OrderRepositoryFactory(ModelRepositoryFactory):
    def __init__(self, pgds):
        from .OrderItem import OrderItemRepositoryFactory
        from .Money import MoneyRepositoryFactory

        self.pgds = pgds
        self.oirf = OrderItemRepositoryFactory(self.pgds)
        self.mrf = MoneyRepositoryFactory(self.pgds)

    def __str__(self):
        data = self.pgds.query(
            'SELECT id, total_cost_id, payment_id, client_id FROM orders')
        if len(data) != 0:
            orders = []
            for row in data:
                orderItems = self.pgds.query(f'''
                    SELECT oi.id, oi.quantity, oi.product_id FROM orders AS o
                    JOIN order_items as oi
                    ON o.id = oi.order_id
                    WHERE o.id = {row[0]}
                ''')
                items_list = [self.oirf.get_order_item(r[0], r[1], r[2], row[0]) for r in orderItems]
                for item in items_list:
                    item.inDB = True
                money = self.mrf.find_by_id(row[2])
                o = self.get_order(row[0], items_list, money, row[3], row[4])
                o.inDB = True
                orders.append(o)
            out = ''
            for order in orders:
                out = out + str(order)
        else:
            out = '\nNo orders here\n'
        return out

    def __repr__(self):
        return str(self.pgds.query(
            'SELECT id, total_cost_id, payment_id, client_id FROM orders'))

    # ##### Factory methods #####
    def get_order(self, id_, items_list, total_cost, payment_id, customer_id):
        return Order(id_, items_list, total_cost, payment_id, customer_id)

    # ##### Repository methods #####
    def all(self):
        res = self.pgds.query(
            'SELECT id, items_ids, total_cost_id, payment_id, client_id FROM orders')
        if len(res) > 0:
            orders = []
            for row in res:
                orderItems = self.pgds.query(f'''
                    SELECT oi.id, oi.quantity, oi.product_id FROM orders AS o
                    JOIN order_items as oi
                    ON o.id = oi.order_id
                    WHERE o.id = {row[0]}
                ''')
                items_list = [self.oirf.get_order_item(r[0], r[1], r[2]) for r in orderItems]
                for item in items_list:
                    item.inDB = True
                money = self.mrf.find_by_id(row[2])
                o = self.get_order(row[0], items_list, money, row[3], row[4])
                o.inDB = True
                orders.append(o)
            return orders
        else:
            return []

    def save(self, order):
        if type(order) != Order: raise TypeError('the entity should only be Order type')
        self.oirf.save_many(order.items_list)
        if order.inDB == False:
            order.id = self.pgds.query(
                f'INSERT INTO orders(created, total_cost_id, payment_id, client_id)\
                VALUES (now(), {order.total_cost.id}, {order.payment_id}, {order.customer_id})\
                RETURNING id')[0][0]
            order.inDB = True
        elif order.inDB:
            self.pgds.query(f'UPDATE orders\
                SET updated = now(), total_cost_id = {order.total_cost.id}, \
                payment_id = {order.payment_id}, client_id = {self.customer_id}\
                WHERE id = {order.id}')

    def save_many(self, *orders):
        # Checking object quantity
        l = len(orders)
        if l in [0, 1]: raise ValueError(f'at least 2 objects can be saved, not {l}')
        # Checking objects type
        for i in range(l):
            if type(orders[i]) != Order:
                raise TypeError( f'object number {i+1} is not a Order type')
        # Save objects data
        [self.save(order) for order in orders]

    def find_by_id(self, id_):
        if type(id_) != int: raise TypeError('id must be int type')
        data = self.pgds.query(
            f'SELECT id, total_cost_id, payment_id, client_id FROM orders\
            WHERE id = {id_}')
        if len(data) > 0:
            orderItems = self.pgds.query(f'''
                SELECT oi.id, oi.quantity, oi.product_id FROM orders AS o
                JOIN order_items as oi
                ON o.id = oi.order_id
                WHERE o.id = {id_}
            ''')
            items_list = [self.oirf.get_order_item(r[0], r[1], r[2]) for r in orderItems]
            for item in items_list:
                item.inDB = True
            money = self.mrf.find_by_id(data[0][2])
            o = self.get_order(data[0][0], items_list, money, data[0][3], data[0][4])
            o.inDB = True
            return o

    def get_by_customer_id(self, customer_id: int) -> Order:
        if type(customer_id) != int: raise ValueError('customer id must an integer value')
        orders = self.pgds.query(f'SELECT id, total_cost_id, payment_id FROM orders WHERE client_id = {customer_id}')
        if len(orders) > 1: raise ValueError('many orders for one customer exist')

    def delete_by_id(self, id_):
        if type(id_) != int: raise TypeError('id must be int')
        order = self.find_by_id(id_)
        [self.oirf.delete_by_id(oi.id) for oi in order.items_list]
        self.pgds.query(f'DELETE FROM orders WHERE id = {id_}')
