class Payment:
    __ids = []

    def __init__(self, method, volume):
        self.id = self.__get_id()
        self.method = method
        self.volume = volume

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
        title = f"--- Payment ---"
        id = f"Id: {self.id}"
        method = f'Method: {self.method}'
        volume = f'Volume: {self.volume}'
        out = f'\n\n{title}\n{id}\n{method}\n{volume}\n\n'
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
        elif name == 'method':
            if type(value) != tuple:
                raise TypeError('method must be tuple type')
            for v in value:
                if type(v) != str:
                    raise TypeError('method must be contain only str objects')
            object.__setattr__(self, name, value)
        elif name == 'volume':
            from Money import Money
            if type(value) != Money:
                raise TypeError('volume must be Money type')
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
        if type(other) == Payment:
            if self.id == other.id:
                return True
            else:
                return False


class PaymentRepositoryFactory:
    def __init__(self):
        self._lastCreatedId = 0
        self._payments = []

    def __str__(self):
        if len(self._payments) != 0:
            out = ''
            for payment in self._payments:
                out = out + str(payment)
        else:
            out = '\nThere are no payments here\n'
        return out

    def __repr__(self):
        return str(self)

    # ##### Factory methods #####
    def getPayment(self, method, volume):
        obj = Payment(method, volume)
        self._lastCreatedId += 1
        obj.id = self._lastCreatedId
        self._payments.append(obj)
        return obj

    def get_last_id(self):
        return f"\n{'-'*10}\n" + 'Last created object id: ' + str(self._lastCreatedId) + f"\n{'-'*10}\n"

    # ##### Repository methods #####
    def all(self):
        return tuple(self._payments)

    def save(self, payment):
        # Type verify
        if type(payment) != Payment:
            raise TypeError('the entity should be only Payment type')
        # Id verify
        if len(self._payments) != 0:
            for p in self._payments:
                if payment == p:
                    raise AttributeError(
                        'a Payment object with this id already exists')
        self._payments.append(payment)

    def save_many(self, payments_list):
        # checking payments_list type
        if type(payments_list) != list:
            raise TypeError('payments you want save should be in the list')
        # checking object quantity
        if len(payments_list) in [0, 1]:
            l = len(payments_list)
            raise ValueError(f'at least 2 objects can be saved, not {l}')
        # checking objects type
        for i in range(len(payments_list)):
            if type(payments_list[i]) != Payment:
                raise TypeError(
                    f'object with index {i} is not a Payment type')
        # checking objects id's
        for payment in payments_list:
            for p in self._payments:
                if payment == p:
                    raise AttributeError(
                        'a Payment object with this id already exists')
        self._payments.extend(payments_list)

    def overwrite(self, payments_list):
        # checking payments_list type
        if type(payments_list) != list:
            raise TypeError(
                'payments you want overwrite should be in the list')
        # checking objects type
        for i in range(len(payments_list)):
            if type(payments_list[i]) != Payment:
                raise TypeError(
                    f'object with index {i} is not a Payment type')
        # checking objects id's
        for payment in payments_list:
            for p in self._money:
                if payment == p:
                    raise AttributeError(
                        'a Payment object with this id already exists')
        self._payments = payments_list

    def findById(self, id_, showMode=True):
        # check type
        if type(id_) != int:
            raise TypeError('id must be int type')
        # search and remove
        for payment in self._payments:
            if payment.id == id_:
                if showMode:
                    return f"\n{'-'*10}\n" + f'Payment found by id [{id_}]:' + str(payment) + f"\n{'-'*10}\n"
                else:
                    return payment
        if showMode:
            return f"\n{'-'*10}\n" + f'Payment found by id [{id_}]:' + '\n\nNothing was found' + f"\n{'-'*10}\n"
        else:
            return payment

    def deleteById(self, id_):
        # check type
        if type(id_) != int:
            raise TypeError('id must be int type')
        # search and remove
        for payment in self._payments:
            if id_ == payment.id:
                self._payments.remove(payment)
    
    def findMethod(self, method, showMode=True):
        # check type
        pass

    def findByMethod(self, method, showMode=True):
        # check type
        if type(method) != str:
            raise TypeError('method must be str type')
        # With a incomplete match with the method
        found = []
        for payment in self._payments:
            for m in payment.method:
                if method in m:
                    found.append(payment)
        if len(found) != 0:
            if showMode:
                out = ''
                for c in found:
                    out = out + str(c)
                return f"\n{'-'*10}\n" + f'Payments found by method keyword \"{method}\":' + out + f"\n{'-'*10}\n"
            else:
                return found
        # With a complete match with the method
        for payment in self._payments:
            for m in payment.method:
                if method == m:
                    if showMode:
                        return f"\n{'-'*10}\n" + f'Found Payment with method \"{method}\":' + str(payment) + f"\n{'-'*10}\n"
                    else:
                        return found
        if showMode:
            return f"\n{'-'*10}\n" + f'Found Payment with method \"{method}\":' + '\n\nNothing was found' + f"\n{'-'*10}\n"
        else:
            return found
    
    def findByVolume(self, moneyId, showMode=True):
        # check type
        if type(moneyId) != int:
            raise TypeError('money id must be int type')
        # search
        found = []
        for payment in self._payments:
            if payment.volume.id == moneyId:
                found.append(payment)
        # output
        if showMode:
            if len(found) == 0:
                return f"\n{'-'*10}\n" + f'Payments found by volume with money id [{moneyId}]:' + f'\n\nNothing was found' + f"\n{'-'*10}\n"
            else:
                out = ''
                for payment in found:
                    out = out + str(payment)
                return f"\n{'-'*10}\n" + f'Payments found by volume with money id [{moneyId}]:' + out + f"\n{'-'*10}\n"
        else:
            return found
