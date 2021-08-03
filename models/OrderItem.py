class OrderItem:
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
        title = f"--- OrderItem ---"
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
                    raise TypeError('can\'t link multiple order items to the same item id')
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
        if type(other) == OrderItem:
            if self.id == other.id:
                return True
            else:
                return False


class OrderItemRepositoryFactory:
    def __init__(self):
        self._lastCreatedId = 0
        self._orderItems = []

    def __str__(self):
        if len(self._orderItems) != 0:
            out = ''
            for orderItem in self._orderItems:
                out = out + str(orderItem)
        else:
            out = '\nThere are no order items here\n'
        return out

    def __repr__(self):
        return str(self)

    # ##### Factory methods #####
    def getOrderItem(self, quantity, itemId):
        obj = OrderItem(quantity, itemId)
        self._lastCreatedId += 1
        obj.id = self._lastCreatedId
        self._orderItems.append(obj)
        return obj

    def get_last_id(self):
        return f"\n{'-'*10}\n" + 'Last created object id: ' + str(self._lastCreatedId) + f"\n{'-'*10}\n"

    # ##### Repository methods #####
    def all(self):
        return tuple(self._orderItems)

    def save(self, orderItem):
        # Type verify
        if type(orderItem) != OrderItem:
            raise TypeError('the entity should be only OrderItem type')
        # Id verify
        if len(self._orderItems) != 0:
            for oi in self._orderItems:
                if orderItem == oi:
                    raise AttributeError(
                        'a OrderItem object with this id already exists')
        self._orderItems.append(orderItem)

    def save_many(self, orderItems_list):
        # checking orderItems_list type
        if type(orderItems_list) != list:
            raise TypeError('order items you want save should be in the list')
        # checking object quantity
        if len(orderItems_list) in [0, 1]:
            l = len(orderItems_list)
            raise ValueError(f'at least 2 objects can be saved, not {l}')
        # checking objects type
        for i in range(len(orderItems_list)):
            if type(orderItems_list[i]) != OrderItem:
                raise TypeError(
                    f'object with index {i} is not a OrderItem type')
        # checking objects id's
        for orderItem in orderItems_list:
            for oi in self._orderItems:
                if orderItem.id == oi.id:
                    raise AttributeError(
                        'a OrderItem object with this id already exists')
        self._orderItems.extend(orderItems_list)

    def overwrite(self, orderItems_list):
        # checking orderItems_list type
        if type(orderItems_list) != list:
            raise TypeError(
                'order items you want overwrite should be in the list')
        # checking objects type
        for i in range(len(orderItems_list)):
            if type(orderItems_list[i]) != OrderItem:
                raise TypeError(
                    f'object with index {i} is not a OrderItem type')
        # checking objects id's
        for orderItem in orderItems_list:
            for oi in self._orderItems:
                if orderItem.id == oi.id:
                    raise AttributeError(
                        'a OrderItem object with this id already exists')
        self._orderItems = orderItems_list

    def findById(self, id_, showMode=True):
        for orderItem in self._orderItems:
            if orderItem.id == id_:
                if showMode:
                    return f"\n{'-'*10}\n" + f'Order item found by id [{id_}]:' + str(orderItem) + f"\n{'-'*10}\n"
                else:
                    return orderItem
        if showMode:
            return f"\n{'-'*10}\n" + f'Order item found by id [{id_}]:' + '\n\nNothing was found' + f"\n{'-'*10}\n"
        else:
            return orderItem

    def findByQuantity(self, quantity, showMode=True):
        # check type
        if type(quantity) != int:
            raise TypeError('quantity must be int type')
        # search
        found = []
        for orderItem in self._orderItems:
            if orderItem.quantity == quantity:
                found.append(orderItem)
        if len(found) != 0:
            if showMode:
                return f"\n{'-'*10}\nFound order items with quantity [{quantity}]: \n{found}\n{'-'*10}"
            else:
                return found
        else:
            if showMode:
                return f"\n{'-'*10}\nFound order items with quantity [{quantity}]: \nNothing was found\n{'-'*10}"
            else:
                return found
    
    def findByQuantityRange(self, quantityMin, quantityMax, showMode=True):
        # check type
        for quantity in [quantityMin, quantityMax]:
            if type(quantity) != int:
                raise TypeError('quantity ranges must be int type')
        # search
        found = []
        for orderItem in self._orderItems:
            if orderItem.quantity >= quantityMin\
                and orderItem.quantity <= quantityMax:
                    found.append(orderItem)
        if len(found) != 0:
            if showMode:
                return f"\n{'-'*10}\nFound order items in quantity range [{quantityMin}-{quantityMax}]: \n{found}\n{'-'*10}"
            else:
                return found
        else:
            if showMode:
                return f"\n{'-'*10}\nFound order items in quantity range [{quantityMin}-{quantityMax}]: \nNothing was found\n{'-'*10}"
            else:
                return found
    
    def findByItemId(self, itemId, showMode=True):
        # check type
        if type(itemId) != int:
            raise TypeError('itemId must be int type')
        # search
        found = []
        for orderItem in self._orderItems:
            if orderItem.itemId == itemId:
                found.append(orderItem)
        if len(found) != 0:
            if showMode:
                return f"\n{'-'*10}\nFound order items with item id [{itemId}]: \n{found}\n{'-'*10}"
            else:
                return found
        else:
            if showMode:
                return f"\n{'-'*10}\nFound order items with item id [{itemId}]: \nNothing was found\n{'-'*10}"
            else:
                return found

    def deleteById(self, id_):
        for orderItem in self._orderItems:
            if id_ == orderItem.id:
                self._orderItems.remove(orderItem)
