class Order:
    def __init__(self, id_, itemsList, totalCost, paymentId, customerId):
        self.id = id_
        self.inDB = False
        self.itemsList = itemsList
        self.totalCost = totalCost
        self.paymentId = paymentId
        self.customerId = customerId

    def __str__(self):
        title = f"--- Order ---"
        id = f"Id: {self.id}"
        inDB = f'In DB: {self.inDB}'
        itemsList = f'Item list: {self.itemsList}'
        totalCost = f'Total cost: {self.totalCost}'
        paymentId = f'Payment id: {self.paymentId}'
        customerId = f'Customer id: {self.customerId}'
        out = f'\n\n{title}\n{id}\n{inDB}\n{itemsList}\n{totalCost}\n{paymentId}\n{customerId}\n\n'
        return out

    def __repr__(self):
        return f'<<{[self.id, self.inDB, self.itemsList, self.totalCost, self.paymentId, self.customerId]}>>'

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
                raise TypeError(
                    'value for inDB attribute must be True or False only')
        elif name == 'itemsList':
            from .OrderItem import OrderItem
            if type(value) != list:
                raise TypeError('itemsList must be list type')
            for v in value:
                if type(v) != OrderItem:
                    raise TypeError('itemsList must be contain only OrderItem type objects')
            object.__setattr__(self, name, value)
        elif name == 'totalCost':
            from .Money import Money
            if type(value) != Money:
                raise TypeError('totalCost must be Money type')
            else:
                object.__setattr__(self, name, value)
        elif name == 'paymentId':
            if type(value) != int:
                raise TypeError('paymentId must be int type')
            else:
                object.__setattr__(self, name, value)
        elif name == 'customerId':
            if type(value) != int:
                raise TypeError('customerId must be int type')
            else:
                object.__setattr__(self, name, value)
        else:
            object.__setattr__(self, name, value)

    def __eq__(self, other):
        if type(other) == Order:
            if self.id == other.id:
                return True
            else:
                return False


class OrderRepositoryFactory:
    def __init__(self, pgds):
        self.pgds = pgds

    def __str__(self):
        data = self.pgds.query(
            'SELECT id, total_cost_id, payment_id, client_id FROM orders')
        if len(data) != 0:
            from .OrderItem import OrderItemRepositoryFactory
            from .Money import MoneyRepositoryFactory
            oirf = OrderItemRepositoryFactory(self.pgds)
            mrf = MoneyRepositoryFactory(self.pgds)
            orders = []
            for row in data:
                orderItems = self.pgds.query(f'''
                    SELECT oi.id, oi.quantity, oi.product_id FROM orders AS o
                    JOIN order_items as oi
                    ON o.id = oi.order_id
                    WHERE o.id = {row[0]}
                ''')
                itemsList = [oirf.getOrderItem(r[0], r[1], r[2]) for r in orderItems]
                for item in itemsList:
                    item.inDB = True
                money = mrf.findById(row[2])
                o = self.getOrder(row[0], itemsList, money, row[3], row[4])
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
    def getOrder(self, id_, itemsList, totalCost, paymentId, customerId):
        return Order(id_, itemsList, totalCost, paymentId, customerId)

    # ##### Repository methods #####
    def all(self):
        res = self.pgds.query(
            'SELECT id, items_ids, total_cost_id, payment_id, client_id FROM orders')
        if len(res) > 0:
            from .OrderItem import OrderItemRepositoryFactory
            from .Money import MoneyRepositoryFactory
            oirf = OrderItemRepositoryFactory(self.pgds)
            mrf = MoneyRepositoryFactory(self.pgds)
            orders = []
            for row in res:
                orderItems = self.pgds.query(f'''
                    SELECT oi.id, oi.quantity, oi.product_id FROM orders AS o
                    JOIN order_items as oi
                    ON o.id = oi.order_id
                    WHERE o.id = {row[0]}
                ''')
                itemsList = [oirf.getOrderItem(r[0], r[1], r[2]) for r in orderItems]
                for item in itemsList:
                    item.inDB = True
                money = mrf.findById(row[2])
                o = self.getOrder(row[0], itemsList, money, row[3], row[4])
                o.inDB = True
                orders.append(o)
            return orders
        else:
            return []

    def save(self, order):
        # Type verify
        if type(order) != Order:
            raise TypeError('the entity should only be Order type')
        # Save object data
        from .OrderItem import OrderItemRepositoryFactory
        oirf = OrderItemRepositoryFactory(self.pgds)
        oirf.save_many(order.itemsList)
        if order.inDB == False:
            order.id = self.pgds.query(
                f'INSERT INTO orders(created, total_cost_id, payment_id, client_id)\
                VALUES (now(), {order.totalCost.id}, {order.paymentId}, {order.customerId})\
                RETURNING id')[0][0]
            order.inDB = True
        elif order.inDB:
            self.pgds.query(f'UPDATE orders\
                SET updated = now(), total_cost_id = {order.totalCost.id}, \
                payment_id = {order.paymentId}, client_id = {self.customerId}\
                WHERE id = {order.id}')

    def save_many(self, *orders):
        # Checking object quantity
        l = len(orders)
        if l in [0, 1]:
            raise ValueError(f'at least 2 objects can be saved, not {l}')
        # Checking objects type
        for i in range(len(orders)):
            if type(orders[i]) != Order:
                raise TypeError( f'object number {i+1} is not a Order type')
        # Save objects data
        from .OrderItem import OrderItemRepositoryFactory
        oirf = OrderItemRepositoryFactory(self.pgds)
        for order in orders:
            oirf.save_many(order.itemsList)
            itemsIds = str([oi.id for oi in order.itemsList]).replace('[', '{')
            itemsIds.replace(']', '}')
            if order.inDB == False:
                order.id = self.pgds.query(
                    f'INSERT INTO orders(created, total_cost_id, payment_id, client_id)\
                    VALUES (now(), {order.totalCost.id}, {order.paymentId}, {order.customerId})\
                    RETURNING id')[0][0]
                order.inDB = True
            elif order.inDB:
                self.pgds.query(f'UPDATE orders\
                    SET updated = now(), items_ids = {itemsIds}, total_cost_id = {order.totalCost.id}, \
                    payment_id = {order.paymentId}, client_id = {self.customerId}\
                    WHERE id = {order.id}')


    def findById(self, id_):
        # Checking type
        if type(id_) != int:
            raise TypeError('id must be int type')
        # Search and return
        data = self.pgds.query(
            f'SELECT id, total_cost_id, payment_id, client_id FROM orders\
            WHERE id = {id_}')
        if len(data) > 0:
            from .OrderItem import OrderItemRepositoryFactory
            from .Money import MoneyRepositoryFactory
            oirf = OrderItemRepositoryFactory(self.pgds)
            mrf = MoneyRepositoryFactory(self.pgds)
            orderItems = self.pgds.query(f'''
                SELECT oi.id, oi.quantity, oi.product_id FROM orders AS o
                JOIN order_items as oi
                ON o.id = oi.order_id
                WHERE o.id = {id_}
            ''')
            itemsList = [oirf.getOrderItem(r[0], r[1], r[2]) for r in orderItems]
            for item in itemsList:
                item.inDB = True
            money = mrf.findById(data[0][2])
            o = self.getOrder(data[0][0], itemsList, money, data[0][3], data[0][4])
            o.inDB = True
            return o

    def deleteById(self, id_):
        # Checking type
        if type(id_) != int:
            raise TypeError('id must be int')
        # Delete from order_items
        from .OrderItem import OrderItemRepositoryFactory
        oirf = OrderItemRepositoryFactory(self.pgds)
        order = self.findById(id_)
        for oi in order.itemsList:
            oirf.deleteById(oi.id)
        # Delete from orders
        self.pgds.query(f'DELETE FROM orders WHERE id = {id_}')
