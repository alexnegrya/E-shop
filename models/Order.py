class Order:
    __ids = []

    def __init__(self, itemList, totalCost, paymentId, customerId):
        self.id = self.__get_id()
        self.itemList = itemList
        self.totalCost = totalCost
        self.paymentId = paymentId
        self.customerId = customerId

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
        title = f"--- Order ---"
        id = f"Id: {self.id}"
        itemList = f'Item list: {self.itemList}'
        totalCost = f'Total cost: {self.totalCost}'
        paymentId = f'Payment id: {self.paymentId}'
        customerId = f'Customer id: {self.customerId}'
        out = f'\n\n{title}\n{id}\n{itemList}\n{totalCost}\n{paymentId}\n{customerId}\n\n'
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
        elif name == '__ids':
            raise AttributeError('changing this attribute is not allowed')
        elif name == 'itemList':
            # from .OrderItem import OrderItem
            if type(value) != list:
                raise TypeError('itemList must be list type')
            # for v in value:
            #     if type(v) != OrderItem:
            #         raise TypeError('itemList must be contain only OrderItem type objects')
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

    def __getattr__(self, name):
        if name == 'id':
            object.__getattribute__(self, str(name))
        elif name == '__ids':
            return tuple(self.__ids)

    def __eq__(self, other):
        if type(other) == Order:
            if self.id == other.id:
                return True
            else:
                return False


class OrderRepositoryFactory:
    def __init__(self):
        self._lastCreatedId = 0
        self._orders = []

    def __str__(self):
        if len(self._orders) != 0:
            out = ''
            for order in self._orders:
                out = out + str(order)
        else:
            out = '\nThere are no orders here\n'
        return out

    def __repr__(self):
        return str(self)

    # ##### Factory methods #####
    def getOrder(self, itemList, totalCost, paymentId, customerId):
        obj = Order(itemList, totalCost, paymentId, customerId)
        self._lastCreatedId += 1
        obj.id = self._lastCreatedId
        self._orders.append(obj)
        return obj

    def get_last_id(self):
        return f"\n{'-'*10}\n" + 'Last created object id: ' + str(self._lastCreatedId) + f"\n{'-'*10}\n"

    # ##### Repository methods #####
    def all(self):
        return tuple(self._orders)

    def save(self, order):
        # Type verify
        if type(order) != Order:
            raise TypeError('the entity should only be Order type')
        # Id verify
        if len(self._orders) != 0:
            for o in self._orders:
                if order == o:
                    raise AttributeError(
                        'a Order object with this id already exists')
        self._orders.append(order)

    def save_many(self, orders_list):
        # checking orders_list type
        if type(orders_list) != list:
            raise TypeError('orders you want save should be in the list')
        # checking object quantity
        if len(orders_list) in [0, 1]:
            l = len(orders_list)
            raise ValueError(f'at least 2 objects can be saved, not {l}')
        # checking objects type
        for i in range(len(orders_list)):
            if type(orders_list[i]) != Order:
                raise TypeError(
                    f'object with index {i} is not a Order type')
        # checking objects id's
        for order in orders_list:
            for o in self._orders:
                if order == o:
                    raise AttributeError(
                        'a Order object with this id already exists')
        self._orders.extend(orders_list)

    def overwrite(self, orders_list):
        # checking orders_list type
        if type(orders_list) != list:
            raise TypeError(
                'orders you want overwrite should be in the list')
        # checking objects type
        for i in range(len(orders_list)):
            if type(orders_list[i]) != Order:
                raise TypeError(
                    f'object with index {i} is not a Order type')
        # checking objects id's
        for order in orders_list:
            for o in self._orders:
                if order == o:
                    raise AttributeError(
                        'a Order object with this id already exists')
        self._orders = orders_list

    def findById(self, id_, showMode=True):
        # check id
        if type(id_) != int:
            raise TypeError('id must be int type')
        # search
        for order in self._orders:
            if order.id == id_:
                if showMode:
                    return f"\n{'-'*10}\n" + f'Order found by id [{id_}]:' + str(order) + f"\n{'-'*10}\n"
                else:
                    return order
        if showMode:
            return f"\n{'-'*10}\n" + f'Order found by id [{id_}]:' + '\n\nNothing was found' + f"\n{'-'*10}\n"
        else:
            return order

    def deleteById(self, id_):
        for order in self._orders:
            if id_ == order.id:
                self._orders.remove(order)

    def findItemById(self, itemId, showMode=True):
        # check type
        if type(itemId) != int:
            raise TypeError('itemId must be int type')
        # search
        found = {}
        for order in self._orders:
            for item in order.itemList:
                if item.id == itemId:
                    found[order.id] = item
        # output
        if len(found) != 0:
            if showMode:
                return f"\n{'-'*10}\n" + f'Items found by item id [{itemId}] in orders with ids: ' + f'\n{found}' + f"\n{'-'*10}\n"
            else:
                return found
        else:
            if showMode:
                return f"\n{'-'*10}\n" + f'Items found by item id [{itemId}] in orders with ids: ' + '\nNothing was found' + f"\n{'-'*10}\n"
            else:
                return found
    
    def findByItemId(self, itemId, showMode=True):
        # check type
        if type(itemId) != int:
            raise TypeError('itemId must be int type')
        # search
        found = []
        for order in self._orders:
            for item in order.itemList:
                if item.id == itemId:
                    found.append(order)
        # output
        if len(found) != 0:
            if showMode:
                return f"\n{'-'*10}\n" + f'Orders found with items with id [{itemId}]: ' + f'\n{found}' + f"\n{'-'*10}\n"
            else:
                return found
        else:
            if showMode:
                return f"\n{'-'*10}\n" + f'Orders found with item with id [{itemId}]: ' + '\nNothing was found' + f"\n{'-'*10}\n"
            else:
                return found
    
    def findByTotalCost(self, moneyId=None, amount=None, currencyId=None, showMode=True):
        # Check type
        args_names = ['moneyId', 'amount', 'currencyId']
        arg_pos = 0
        m = None
        a = None
        c = None
        for argument in (moneyId, amount, currencyId):
            if argument != None:
                if type(argument) != int:
                    raise TypeError(f'{args_names[arg_pos]} must be int type')
                if m == None:
                    m = True if arg_pos == 0 else False
                if a == None and arg_pos != 0:
                    a = True if arg_pos == 1 else False
                if c == None and arg_pos not in (0, 1):
                    c = True if arg_pos == 2 else False
            arg_pos += 1
        # Search
        # variants: [m], [a], [c], [m, c], [a, m], [a, c], [m, a, c]
        found = []
        if m and a and c:
            for order in self._orders:
                if order.totalCost.id == moneyId\
                    and order.totalCost.amount == amount\
                        and order.totalCost.currencyId == currencyId:
                    found.append(order)
            args = ''
            for arg in args_names:
                if arg == 'moneyId':
                    args = args + arg + f' - {moneyId}, '
                elif arg == 'amount':
                    args = args + arg + f' - {amount}, '
                else:
                    args = args + arg + f' - {currencyId}'
        elif a and m:
            for order in self._orders:
                if order.totalCost.amount == amount\
                    and order.totalCost.id == moneyId:
                    found.append(order)
            args_names.pop(2)
            args_names.reverse()
            args = ''
            for arg in args_names:
                if arg == 'amount':
                    args = args + arg + f' - {amount}, '
                else:
                    args = args + arg + f' - {moneyId}'
        elif a and c:
            for order in self._orders:
                if order.totalCost.amount == amount\
                    and order.totalCost.currencyId == currencyId:
                    found.append(order)
            args_names.pop(0)
            args = ''
            for arg in args_names:
                if arg == 'amount':
                    args = args + arg + f' - {amount}, '
                else:
                    args = args + arg + f' - {currencyId}'
        elif m and c:
            for order in self._orders:
                if order.totalCost.id == moneyId\
                    and order.totalCost.currencyId == currencyId:
                    found.append(order)
            args_names.pop(1)
            args = ''
            for arg in args_names:
                if arg == 'moneyId':
                    args = args + arg + f' - {moneyId}, '
                else:
                    args = args + arg + f' - {currencyId}'
        elif m:
            for order in self._orders:
                if order.totalCost.id == moneyId:
                    found.append(order)
            args_names.pop(1)
            args_names.pop(1)
            args = args_names[0] + f' - {moneyId}'
        elif a:
            for order in self._orders:
                if order.totalCost.amount == amount:
                    found.append(order)
            args_names.pop(0)
            args_names.pop(1)
            args = args_names[0] + f' - {amount}'
        elif c:
            for order in self._orders:
                if order.totalCost.currencyId == currencyId:
                    found.append(order)
            args_names.pop(0)
            args_names.pop(0)
            args = args_names[0] + f' - {currencyId}'
        else:
            raise ValueError('at least one argument must be specified')
        # Output
        if len(found) != 0:
            if showMode:
                return f"\n{'-'*10}\n" + f'Orders found by total cost {args}:' + f'\n{found}' + f"\n{'-'*10}\n"
            else:
                return found
        else:
            if showMode:
                return f"\n{'-'*10}\n" + f'Orders found by total cost {args}:' + '\nNothing was found' + f"\n{'-'*10}\n"
            else:
                return found
    
    def findByPaymentId(self, paymentId, showMode=True):
        # check type
        if type(paymentId) != int:
            raise TypeError('paymentId must be int type')
        # search
        found = []
        for order in self._orders:
            if order.paymentId == paymentId:
                found.append(order)
        # output
        if len(found) != 0:
            if showMode:
                return f"\n{'-'*10}\n" + f'Orders found by payment id {paymentId}:' + f'\n{found}' + f"\n{'-'*10}\n"
            else:
                return found
        else:
            if showMode:
                return f"\n{'-'*10}\n" + f'Orders found by payment id {paymentId}:' + '\nNothing was found' + f"\n{'-'*10}\n"
            else:
                return found

    def findByCustomerId(self, customerId, showMode=True):
        # check type
        if type(customerId) != int:
            raise TypeError('customerId must be int type')
        # search
        found = []
        for order in self._orders:
            if order.customerId == customerId:
                found.append(order)
        # output
        if len(found) != 0:
            if showMode:
                return f"\n{'-'*10}\n" + f'Orders found by customer id {customerId}:' + f'\n{found}' + f"\n{'-'*10}\n"
            else:
                return found
        else:
            if showMode:
                return f"\n{'-'*10}\n" + f'Orders found by customer id {customerId}:' + '\nNothing was found' + f"\n{'-'*10}\n"
            else:
                return found
