class OrderItem:
    def __init__(self, id_, quantity, itemId):
        self.id = id_
        self.inDB = False
        self.quantity = quantity
        self.itemId = itemId

    def __str__(self):
        title = f"--- OrderItem ---"
        id = f"Id: {self.id}"
        inDB = f'In DB: {self.inDB}'
        quantity = f'Quantity: {self.quantity}'
        itemId = f'Item id: {self.itemId}'
        return f'\n\n{title}\n{id}\n{inDB}\n{quantity}\n{itemId}\n\n'

    def __repr__(self):
        return f'<<{[self.id, self.inDB, self.quantity, self.itemId]}>>'

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
        elif name == 'quantity':
            if type(value) != int:
                raise TypeError('wrong type of quantity/itemId attribute')
            else:
                object.__setattr__(self, name, value)
        elif name == 'itemId':
            if type(value) != int:
                raise TypeError('wrong type of quantity/itemId attribute')
            else:
                if value not in self.__itemsIds:
                    self.__itemsIds.append(value)
                    object.__setattr__(self, name, value)
                else:
                    raise TypeError('can\'t link multiple order items to the same item id')
        else:
            object.__setattr__(self, name, value)

    def __eq__(self, other):
        if type(other) == OrderItem:
            if self.id == other.id:
                return True
            else:
                return False


class OrderItemRepositoryFactory:
    def __init__(self, pgds):
        self.pgds = pgds

    def __str__(self):
        data = self.pgds.query('SELECT * FROM order_items')
        if len(data) != 0:
            orderItems = []
            for row in data:
                oi = self.getOrderItem(row[0], row[1], row[2])
                oi.inDB = True
                orderItems.append(oi)
            out = ''
            for orderItem in orderItems:
                out = out + str(orderItem)
        else:
            out = '\nNo addresses here\n'
        return out

    def __repr__(self):
        return str(self.pgds.query('SELECT * FROM order_items'))

    # ##### Factory methods #####
    def getOrderItem(self, id_, quantity, itemId):
        return OrderItem(id_, quantity, itemId)

    # ##### Repository methods #####
    def all(self):
        res = self.pgds.query('SELECT * FROM order_items')
        if len(res) > 0:
            orderItems = []
            for row in res:
                oi = self.getOrderItem(row[0], row[1], row[2])
                oi.inDB = True
                orderItems.append(oi)
            return orderItems
        else:
            return []

    def save(self, orderItem):
        # Type verify
        if type(orderItem) != OrderItem:
            raise TypeError('the entity should be only OrderItem type')
        # Save object data
        if orderItem.inDB == False:
            orderItem.id = self.pgds.query(f'INSERT INTO order_items(quantity, product_id)\
                VALUES ({orderItem.quantity}, {orderItem.product_id})\
                RETURNING id')[0][0]
            orderItem.inDB = True
        elif orderItem.inDB:
            self.pgds.query(f'UPDATE order_items\
                SET quantity = {orderItem.quantity}, product_id = {orderItem.productId}\
                WHERE id = {orderItem.id}')

    def save_many(self, *orderItems):
        # Checking object quantity
        l = len(orderItems)
        if l in [0, 1]:
            raise ValueError(f'at least 2 objects can be saved, not {l}')
        # Checking objects type
        for i in range(len(orderItems)):
            if type(orderItems[i]) != OrderItem:
                raise TypeError(f'object number {i+1} is not a OrderItem type')
        # Save objects data
        for orderItem in orderItems:
            if orderItem.inDB == False:
                orderItem.id = self.pgds.query(f'INSERT INTO order_items(quantity, product_id)\
                    VALUES ({orderItem.quantity}, {orderItem.product_id})\
                    RETURNING id')[0][0]
                orderItem.inDB = True
            elif orderItem.inDB:
                self.pgds.query(f'UPDATE order_items\
                    SET quantity = {orderItem.quantity}, product_id = {orderItem.productId}\
                    WHERE id = {orderItem.id}')

    def findById(self, id_):
        # Checking type
        if type(id_) != int:
            raise TypeError('id must be int type')
        # Search and return
        data = self.pgds.query(f'SELECT * FROM order_items WHERE id = {id_}')
        if len(data) > 0:
            oi = self.getOrderItem(data[0][0], data[0][1], data[0][2])
            oi.inDB = True
            return oi

    def deleteById(self, id_):
        # Checking type
        if type(id_) != int:
            raise TypeError('id must be int value')
        # Delete data
        self.pgds.query(f'DELETE FROM order_items WHERE id = {id_}')
