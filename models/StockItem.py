class StockItem:
    __ids = []
    __itemIds = []

    def __init__(self, quantity, itemId):
        self.id = self.__get_id()
        self.quantity = quantity
        self.itemId = itemId

    def __get_id(self):
        from random import randint
        ID = ''
        for v in range(randint(4, 6)):
            ID = ID + str(randint(0, 9))
        return int(ID)

    def __check_id(self, id_):
        if id_ not in self.__ids:
            if id_ < 1 or id_ > 1000000:
                raise ValueError(
                    'id must be greater then 0 and lesser then 1000000')
            elif type(id_) != int:
                raise TypeError('id must be an integer')
            else:
                return True
        else:
            return False

    def __str__(self):
        title = f"--- StockItem ---"
        id = f"Id: {self.id}"
        quantity = f'Quantity: {self.quantity}'
        itemId = f'Item id: {self.itemId}'
        out = f'\n\n{title}\n{id}\n{quantity}\n{itemId}\n\n'
        return out

    def __repr__(self):
        return str(self)

    def __setattr__(self, name, value):
        if name == 'id':
            if self.__check_id(value):
                object.__setattr__(self, name, value)
            else:
                while True:
                    if value == self.id:
                        if self.__check_id(value):
                            self.id = self.__get_id()
                    else:
                        break
                object.__setattr__(self, name, value)
        elif name in ['__ids', '__itemIds']:
            raise AttributeError('changing this attribute is not allowed')
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

    def __getattr__(self, name):
        if name == 'id':
            object.__getattribute__(self, str(name))
        elif name == '__ids':
            return tuple(self.__ids)
        elif name == '__itemIds':
            return tuple(self.__itemIds)

    def __eq__(self, other):
        if type(other) == StockItem:
            if self.id == other.id:
                return True
            else:
                return False


class StockItemRepositoryFactory:
    def __init__(self):
        self._lastCreatedId = 0
        self._stockItems = []

    def __str__(self):
        if len(self._stockItems) != 0:
            out = ''
            for stockItem in self._stockItems:
                out = out + str(stockItem)
        else:
            out = '\nThere are no stock items here\n'
        return out

    def __repr__(self):
        return str(self)

    # ##### Factory methods #####
    def getStockItem(self, quantity, itemId):
        obj = StockItem(quantity, itemId)
        self._lastCreatedId += 1
        obj.id = self._lastCreatedId
        self._stockItems.append(obj)
        return obj

    def get_last_id(self):
        return f"\n{'-'*10}\n" + 'Last created object id: ' + str(self._lastCreatedId) + f"\n{'-'*10}\n"

    # ##### Repository methods #####
    def all(self):
        return tuple(self._stockItems)

    def save(self, stockItem):
        # Type verify
        if type(stockItem) != StockItem:
            raise TypeError('the entity should be only StockItem type')
        # Id verify
        if len(self._stockItems) != 0:
            for si in self._stockItems:
                if stockItem == si:
                    raise AttributeError(
                        'a StockItem object with this id already exists')
        self._stockItems.append(stockItem)

    def save_many(self, stockItems_list):
        # checking stockItems_list type
        if type(stockItems_list) != list:
            raise TypeError('order items you want save should be in the list')
        # checking object quantity
        if len(stockItems_list) in [0, 1]:
            l = len(stockItems_list)
            raise ValueError(f'at least 2 objects can be saved, not {l}')
        # checking objects type
        for i in range(len(stockItems_list)):
            if type(stockItems_list[i]) != StockItem:
                raise TypeError(
                    f'object with index {i} is not a StockItem type')
        # checking objects id's
        for stockItem in stockItems_list:
            for si in self._stockItems:
                if stockItem == si:
                    raise AttributeError(
                        'a StockItem object with this id already exists')
        self._stockItems.extend(stockItems_list)

    def overwrite(self, stockItems_list):
        # checking stockItems_list type
        if type(stockItems_list) != list:
            raise TypeError('order items you want save should be in the list')
        # checking object quantity
        if len(stockItems_list) in [0, 1]:
            l = len(stockItems_list)
            raise ValueError(f'at least 2 objects can be saved, not {l}')
        # checking objects type
        for i in range(len(stockItems_list)):
            if type(stockItems_list[i]) != StockItem:
                raise TypeError(
                    f'object with index {i} is not a StockItem type')
        # checking objects id's
        for stockItem in stockItems_list:
            for si in self._stockItems:
                if stockItem == si:
                    raise AttributeError(
                        'a StockItem object with this id already exists')
        self._stockItems = stockItems_list

    def findById(self, id_, showMode=True):
        for stockItem in self._stockItems:
            if stockItem.id == id_:
                if showMode:
                    return f"\n{'-'*10}\n" + f'Stock item found by id [{id_}]:' + str(stockItem) + f"\n{'-'*10}\n"
                else:
                    return stockItem
        if showMode:
            return f"\n{'-'*10}\n" + f'Stock item found by id [{id_}]:' + '\n\nNothing was found' + f"\n{'-'*10}\n"
        else:
            return stockItem

    def findByQuantity(self, quantity, showMode=True):
        # check type
        if type(quantity) != int:
            raise TypeError('quantity must be int type')
        # search
        found = []
        for stockItem in self._stockItems:
            if stockItem.quantity == quantity:
                found.append(stockItem)
        if len(found) != 0:
            if showMode:
                return f"\n{'-'*10}\nFound stock items with quantity [{quantity}]: \n{found}\n{'-'*10}"
            else:
                return found
        else:
            if showMode:
                return f"\n{'-'*10}\nFound stock items with quantity [{quantity}]: \nNothing was found\n{'-'*10}"
            else:
                return found

    def findByQuantityRange(self, quantityMin, quantityMax, showMode=True):
        # check type
        for quantity in [quantityMin, quantityMax]:
            if type(quantity) != int:
                raise TypeError('quantity ranges must be int type')
        # search
        found = []
        for stockItem in self._stockItems:
            if stockItem.quantity >= quantityMin\
                    and stockItem.quantity <= quantityMax:
                found.append(stockItem)
        if len(found) != 0:
            if showMode:
                return f"\n{'-'*10}\nFound stock items in quantity range [{quantityMin}-{quantityMax}]: \n{found}\n{'-'*10}"
            else:
                return found
        else:
            if showMode:
                return f"\n{'-'*10}\nFound stock items in quantity range [{quantityMin}-{quantityMax}]: \nNothing was found\n{'-'*10}"
            else:
                return found

    def findByItemId(self, itemId, showMode=True):
        # check type
        if type(itemId) != int:
            raise TypeError('itemId must be int type')
        # search
        found = []
        for stockItem in self._stockItems:
            if stockItem.itemId == itemId:
                found.append(stockItem)
        if len(found) != 0:
            if showMode:
                return f"\n{'-'*10}\nFound stock items with item id [{itemId}]: \n{found}\n{'-'*10}"
            else:
                return found
        else:
            if showMode:
                return f"\n{'-'*10}\nFound stock items with item id [{itemId}]: \nNothing was found\n{'-'*10}"
            else:
                return found

    def deleteById(self, id_):
        for stockItem in self._stockItems:
            if id_ == stockItem.id:
                self._stockItems.remove(stockItem)
