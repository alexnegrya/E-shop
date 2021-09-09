class StockItem:
    def __init__(self, id_, quantity, itemId):
        self.id = id_
        self.inDB = False
        self.quantity = quantity
        self.itemId = itemId

    def __str__(self):
        title = f"--- StockItem ---"
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
                raise TypeError(
                    'value for inDB attribute must be True or False only')
        elif name == 'quantity':
            if type(value) != int:
                raise TypeError('wrong type of quantity/itemId attribute')
            else:
                object.__setattr__(self, name, value)
        elif name == 'itemId':
            if type(value) != int:
                raise TypeError('wrong type of quantity/itemId attribute')
            else:
                if value not in self.__itemIds:
                    self.__itemIds.append(value)
                    object.__setattr__(self, name, value)
                else:
                    raise TypeError(
                        'can\'t link multiple order items to the same item id')
        else:
            object.__setattr__(self, name, value)

    def __eq__(self, other):
        if type(other) == StockItem:
            if self.id == other.id:
                return True
            else:
                return False


class StockItemRepositoryFactory:
    def __init__(self, pgds):
        self.pgds = pgds

    def __str__(self):
        stockItems = self.pgds.query('SELECT * FROM stock_items')
        if len(stockItems) != 0:
            sI = []
            for row in stockItems:
                si = self.getStockItem(row[0], row[1], row[2])
                si.inDB = True
                sI.append(si)
            out = ''
            for stockItem in sI:
                out = out + str(stockItem)
        else:
            out = '\nNo addresses here\n'
        return out

    def __repr__(self):
        return str(self.pgds.query('SELECT * FROM stock_items'))

    # ##### Factory methods #####
    def getStockItem(self, id_, quantity, itemId):
        return StockItem(id_, quantity, itemId)

    # ##### Repository methods #####
    def all(self):
        stockItems = self.pgds.query('SELECT * FROM stock_items')
        if len(stockItems) != 0:
            sI = []
            for row in stockItems:
                si = self.getStockItem(row[0], row[1], row[2])
                si.inDB = True
                sI.append(si)
            return sI
        else:
            return []

    def save(self, stockItem):
        # Type verify
        if type(stockItem) != StockItem:
            raise TypeError('the entity should be only StockItem type')
        # Save object data
        if stockItem.inDB == False:
            stockItem.id = self.pgds.query(f'INSERT INTO stock_items(quantity, product_id)\
                VALUES ({stockItem.quantity}, {stockItem.itemId})\
                RETURNING id')[0][0]
            stockItem.inDB = True
        elif stockItem.inDB:
            self.pgds.query(f'UPDATE stock_items\
                SET quantity = {stockItem.quantity}, product_id = {stockItem.itemId}, \
                WHERE id = {stockItem.id}')

    def save_many(self, *stockItems):
        # Checking object quantity
        l = len(stockItems)
        if l in [0, 1]:
            raise ValueError(f'at least 2 objects can be saved, not {l}')
        # Checking objects type
        for i in range(len(stockItems)):
            if type(stockItems[i]) != StockItem:
                raise TypeError(f'object number {i+1} is not a StockItem type')
        # Save objects data
        for stockItem in stockItems:
            if stockItem.inDB == False:
                stockItem.id = self.pgds.query(f'INSERT INTO stock_items(quantity, product_id)\
                    VALUES ({stockItem.quantity}, {stockItem.itemId})\
                    RETURNING id')[0][0]
                stockItem.inDB = True
            elif stockItem.inDB:
                self.pgds.query(f'UPDATE stock_items\
                    SET quantity = {stockItem.quantity}, product_id = {stockItem.itemId}, \
                    WHERE id = {stockItem.id}')

    def findById(self, id_):
        # Checking type
        if type(id_) != int:
            raise TypeError('id must be int')
        # Search and return
        data = self.pgds.query(f'SELECT * FROM stock_items WHERE id = {id_}')
        if len(data) > 0:
            si = self.getStockItem(data[0][0], data[0][1], data[0][2])
            si.inDB = True
            return si

    def deleteById(self, id_):
        # Checking type
        if type(id_) != int:
            raise TypeError('id must be int')
        # Delete data
        self.pgds.query(f'DELETE FROM stock_items WHERE id = {id_}')
