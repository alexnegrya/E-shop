class Service:
    __ids = []

    def __init__(self, name, price):
        self.id = self.__get_id()
        self.name = name
        self.price = price

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
        title = f"--- Service \"{self.name}\" ---"
        id = f"Id: {self.id}"
        price = f'Price: {self.price}'
        return f'\n\n{title}\n{id}\n{price}\n\n'

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
        elif name == 'name':
            if type(value) != str:
                raise TypeError('name must be a string')
            elif value == '':
                raise NameError('name cannot be an empty string')
            else:
                # Spliting name by letters
                splited = []
                for i in range(len(value)):
                    splited.append(value[i])
                # Checking name for letters repition
                repeated_numbers = {}
                for i in range(len(splited)):
                    if splited[i] not in repeated_numbers:
                        repeated_numbers[splited[i]] = 1
                    else:
                        repeated_numbers[splited[i]] += 1
                # Checking name for the same letters only
                for i in range(len(repeated_numbers)):
                    if repeated_numbers[splited[i]] == len(value):
                        raise NameError(
                            'the name contains only the same letters')
                # Cheking name for numbers
                for letter in splited:
                    try:
                        int(letter)
                        raise NameError(
                            'the name must not contain integer values')
                    except ValueError:
                        pass
                object.__setattr__(self, name, value)
        elif name == 'price':
            from .Money import Money
            # check type
            if type(value) != Money:
                raise TypeError('price must be Money type')
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
        if type(other) == Service:
            if self.id == other.id:
                return True
            else:
                return False


class ServiceRepositoryFactory:
    def __init__(self):
        self._lastCreatedId = 0
        self._services = []

    def __str__(self):
        if len(self._services) != 0:
            out = ''
            for service in self._services:
                out = out + str(service)
        else:
            out = '\nThere are no services here\n'
        return out

    def __repr__(self):
        return str(self)

    # ##### Factory methods #####
    def getService(self, name, price):
        obj = Service(name, price)
        self._lastCreatedId += 1
        obj.id = self._lastCreatedId
        self._services.append(obj)
        return obj

    def get_last_id(self):
        return f"\n{'-'*10}\n" + 'Last created object id: ' + str(self._lastCreatedId) + f"\n{'-'*10}\n"

    # ##### Repository methods #####
    def all(self):
        return tuple(self._services)

    def save(self, service):
        # Type verify
        if type(service) != Service:
            raise TypeError('the entity should only be Service type')
        # Id verify
        if len(self._services) != 0:
            for s in self._services:
                if service == s:
                    raise AttributeError(
                        'a Service object with this id already exists')
        self._services.append(service)

    def save_many(self, services_list):
        # checking services_list type
        if type(services_list) != list:
            raise TypeError('services you want save should be in the list')
        # checking object quantity
        if len(services_list) in [0, 1]:
            l = len(services_list)
            raise ValueError(f'at least 2 objects can be saved, not {l}')
        # checking objects type
        for i in range(len(services_list)):
            if type(services_list[i]) != Service:
                raise TypeError(
                    f'object with index {i} is not a Service type')
        # checking objects id's
        for service in services_list:
            for s in self._services:
                if service == s:
                    raise AttributeError(
                        'a Service object with this id already exists')
        self._services.extend(services_list)

    def overwrite(self, services_list):
        # checking services_list type
        if type(services_list) != list:
            raise TypeError(
                'services you want overwrite should be in the list')
        # checking objects type
        for i in range(len(services_list)):
            if type(services_list[i]) != Service:
                raise TypeError(
                    f'object with index {i} is not a Service type')
        # checking objects id's
        for service in services_list:
            for s in self._services:
                if service == s:
                    raise AttributeError(
                        'a Service object with this id already exists')
        self._services = services_list

    def findById(self, id_, showMode=True):
        if type(id_) != int:
            raise TypeError('id must be int type')
        for service in self._services:
            if service.id == id_:
                if showMode:
                    return f"\n{'-'*10}\n" + f'Service found by id [{id_}]:' + str(service) + f"\n{'-'*10}\n"
                else:
                    return service
        if showMode:
            return f"\n{'-'*10}\n" + f'Service found by id [{id_}]:' + '\n\nNothing was found' + f"\n{'-'*10}\n"
        else:
            return service

    def findByName(self, name, showMode=True):
        if type(name) != str:
            raise TypeError('name must be str type')
        # With a incomplete match with the name
        found = []
        for service in self._services:
            if name in service.name:
                found.append(service)
        if len(found) != 0:
            if showMode:
                out = ''
                for p in found:
                    out = out + str(p)
                return f"\n{'-'*10}\n" + f'Services found by name keyword \"{name}\":' + out + f"\n{'-'*10}\n"
            else:
                return found
        # With a complete match with the name
        for service in self._services:
            if service.name == name:
                if showMode:
                    return f"\n{'-'*10}\n" + f'Found Service with name \"{name}\":' + str(service) + f"\n{'-'*10}\n"
                else:
                    return found
        if showMode:
            return f"\n{'-'*10}\n" + f'Found Service with name \"{name}\":' + '\n\nNothing was found' + f"\n{'-'*10}\n"
        else:
            return found

    def findByPrice(self, price, showMode=True):
        if type(price) != int:
            raise TypeError('price must be int type')
        # search
        found = []
        for service in self._services:
            if service.price == price:
                found.append(service)
        # output
        if showMode:
            if len(found) == 0:
                return f"\n{'-'*10}\n" + f'Services found by price [{price}]:' + f'\n\nNothing was found' + f"\n{'-'*10}\n"
            else:
                out = ''
                for service in found:
                    out = out + str(service)
                return f"\n{'-'*10}\n" + f'Services found by price [{price}]:' + out + f"\n{'-'*10}\n"
        else:
            return found

    def findByPrice(self, moneyId=None, amount=None, currencyId=None, showMode=True):
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
            for service in self._services:
                if service.price.id == moneyId\
                    and service.price.amount == amount\
                        and service.price.currencyId == currencyId:
                    found.append(service)
            args = ''
            for arg in args_names:
                if arg == 'moneyId':
                    args = args + arg + f' - {moneyId}, '
                elif arg == 'amount':
                    args = args + arg + f' - {amount}, '
                else:
                    args = args + arg + f' - {currencyId}'
        elif a and m:
            for service in self._services:
                if service.price.amount == amount\
                        and service.price.id == moneyId:
                    found.append(service)
            args_names.pop(2)
            args_names.reverse()
            args = ''
            for arg in args_names:
                if arg == 'amount':
                    args = args + arg + f' - {amount}, '
                else:
                    args = args + arg + f' - {moneyId}'
        elif a and c:
            for service in self._services:
                if service.price.amount == amount\
                        and service.price.currencyId == currencyId:
                    found.append(service)
            args_names.pop(0)
            args = ''
            for arg in args_names:
                if arg == 'amount':
                    args = args + arg + f' - {amount}, '
                else:
                    args = args + arg + f' - {currencyId}'
        elif m and c:
            for service in self._services:
                if service.price.id == moneyId\
                        and service.price.currencyId == currencyId:
                    found.append(service)
            args_names.pop(1)
            args = ''
            for arg in args_names:
                if arg == 'moneyId':
                    args = args + arg + f' - {moneyId}, '
                else:
                    args = args + arg + f' - {currencyId}'
        elif m:
            for service in self._services:
                if service.price.id == moneyId:
                    found.append(service)
            args_names.pop(1)
            args_names.pop(1)
            args = args_names[0] + f' - {moneyId}'
        elif a:
            for service in self._services:
                if service.price.amount == amount:
                    found.append(service)
            args_names.pop(0)
            args_names.pop(1)
            args = args_names[0] + f' - {amount}'
        elif c:
            for service in self._services:
                if service.price.currencyId == currencyId:
                    found.append(service)
            args_names.pop(0)
            args_names.pop(0)
            args = args_names[0] + f' - {currencyId}'
        else:
            raise ValueError('at least one argument must be specified')
        # Output
        if len(found) != 0:
            if showMode:
                return f"\n{'-'*10}\n" + f'Services found by price {args}:' + f'\n{found}' + f"\n{'-'*10}\n"
            else:
                return found
        else:
            if showMode:
                return f"\n{'-'*10}\n" + f'Services found by price {args}:' + '\nNothing was found' + f"\n{'-'*10}\n"
            else:
                return found

    def deleteById(self, id_):
        if type(id_) != int:
            raise TypeError('id must be int type')
        for service in self._services:
            if id_ == service.id:
                self._services.remove(service)
