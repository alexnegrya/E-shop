class Money:
    __ids = []

    def __init__(self, amount, currencyId, currency=None):
        self.id = self.__get_id()
        self.amount = amount
        self.currencyId = currencyId
        self.currency = currency

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
        title = f"--- Money ---"
        id = f"Id: {self.id}"
        amount = f'Amount: {self.amount}'
        currencyId = f'Currency id: {self.currencyId}'
        out = f'\n\n{title}\n{id}\n{amount}\n{currencyId}\n\n'
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
        elif name == 'amount':
            if type(value) not in (int, float):
                raise TypeError('amount must be int or float type')
            else:
                object.__setattr__(self, name, value)
        elif name == 'currencyId':
            if type(value) not in [int, str]:
                raise TypeError('wrong type of quantity/itemId attribute')
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
        if type(other) == Money:
            if self.id == other.id:
                return True
            else:
                return False


class MoneyRepositoryFactory:
    def __init__(self):
        self._lastCreatedId = 0
        self._money = []

    def __str__(self):
        if len(self._money) != 0:
            out = ''
            for money in self._money:
                out = out + str(money)
        else:
            out = '\nThere are no money here\n'
        return out

    def __repr__(self):
        return str(self)

    # ##### Factory methods #####
    def getMoney(self, amount, currencyId):
        obj = Money(amount, currencyId)
        self._lastCreatedId += 1
        obj.id = self._lastCreatedId
        self._money.append(obj)
        return obj

    def get_last_id(self):
        return f"\n{'-'*10}\n" + 'Last created object id: ' + str(self._lastCreatedId) + f"\n{'-'*10}\n"

    # ##### Repository methods #####
    def all(self):
        return tuple(self._money)

    def save(self, money):
        # Type verify
        if type(money) != Money:
            raise TypeError('the entity should be only Money type')
        # Id verify
        if len(self._money) != 0:
            for m in self._money:
                if money == m:
                    raise AttributeError(
                        'a Money object with this id already exists')
        self._money.append(money)

    def save_many(self, money_list):
        # checking money_list type
        if type(money_list) != list:
            raise TypeError('money you want save should be in the list')
        # checking object quantity
        if len(money_list) in [0, 1]:
            l = len(money_list)
            raise ValueError(f'at least 2 objects can be saved, not {l}')
        # checking objects type
        for i in range(len(money_list)):
            if type(money_list[i]) != Money:
                raise TypeError(
                    f'object with index {i} is not a Money type')
        # checking objects id's
        for money in money_list:
            for m in self._money:
                if money.id == m.id:
                    raise AttributeError(
                        'a Money object with this id already exists')
        self._money.extend(money_list)

    def overwrite(self, money_list):
        # checking money_list type
        if type(money_list) != list:
            raise TypeError(
                'money you want overwrite should be in the list')
        # checking objects type
        for i in range(len(money_list)):
            if type(money_list[i]) != Money:
                raise TypeError(
                    f'object with index {i} is not a Money type')
        # checking objects id's
        for money in money_list:
            for m in self._money:
                if money.id == m.id:
                    raise AttributeError(
                        'a Money object with this id already exists')
        self._money = money_list

    def findById(self, id_, showMode=True):
        # check type
        if type(id_) != int:
            raise TypeError('id must be int type')
        # search and remove
        for money in self._money:
            if money.id == id_:
                if showMode:
                    return f"\n{'-'*10}\n" + f'Money found by id [{id_}]:' + str(money) + f"\n{'-'*10}\n"
                else:
                    return money
        if showMode:
            return f"\n{'-'*10}\n" + f'Money found by id [{id_}]:' + '\n\nNothing was found' + f"\n{'-'*10}\n"
        else:
            return money

    def findByAmount(self, amount, showMode=True):
        # check type
        if type(amount) != int:
            raise TypeError('amount must be int type')
        # search
        found = []
        for money in self._money:
            if money.amount == amount:
                found.append(money)
        if len(found) != 0:
            if showMode:
                return f"\n{'-'*10}\nFound money with amount [{amount}]: \n{found}\n{'-'*10}"
            else:
                return found
        else:
            if showMode:
                return f"\n{'-'*10}\nFound money with amount [{amount}]: \nNothing was found\n{'-'*10}"
            else:
                return found

    def findByAmountRange(self, amountMin, amountMax, showMode=True):
        # check type
        for amount in [amountMin, amountMax]:
            if type(amount) != int:
                raise TypeError('amount ranges must be int type')
        # search
        found = []
        for money in self._money:
            if money.amount >= amountMin\
                    and money.amount <= amountMax:
                found.append(money)
        if len(found) != 0:
            if showMode:
                return f"\n{'-'*10}\nFound money in amount range [{amountMin}-{amountMax}]: \n{found}\n{'-'*10}"
            else:
                return found
        else:
            if showMode:
                return f"\n{'-'*10}\nFound money in amount range [{amountMin}-{amountMax}]: \nNothing was found\n{'-'*10}"
            else:
                return found

    def findByCurrencyId(self, currencyId, showMode=True):
        # check type
        if type(currencyId) != int:
            raise TypeError('currencyId must be int type')
        # search
        found = []
        for money in self._money:
            if money.currencyId == currencyId:
                found.append(money)
        if len(found) != 0:
            if showMode:
                return f"\n{'-'*10}\nFound money with currency id [{currencyId}]: \n{found}\n{'-'*10}"
            else:
                return found
        else:
            if showMode:
                return f"\n{'-'*10}\nFound money with currency id [{currencyId}]: \nNothing was found\n{'-'*10}"
            else:
                return found

    def deleteById(self, id_):
        # check type
        if type(id_) != int:
            raise TypeError('id must be int type')
        # search and remove
        for money in self._money:
            if id_ == money.id:
                self._money.remove(money)
