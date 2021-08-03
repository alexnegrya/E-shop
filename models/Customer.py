class Customer:
    __ids = []

    def __init__(self, firstName, lastName, addressId):
        self.id = self.__get_id()
        self.firstName = firstName
        self.lastName = lastName
        self.addressId = addressId
    
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
        title = f"--- Customer ---"
        id = f"Id: {self.id}"
        firstName = f'First name: {self.firstName}'
        lastName = f'Last name: {self.lastName}'
        address = f'Address id: {self.addressId}'
        out = '\n\n' + title + '\n' + id + '\n'\
            + firstName + '\n' + lastName + '\n' + address + '\n\n'
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
        elif name == 'firstName' or name == 'lastName':
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
                repeat_numbers = {}
                for i in range(len(splited)):
                    if splited[i] not in repeat_numbers:
                        repeat_numbers[splited[i]] = 1
                    else:
                        repeat_numbers[splited[i]] += 1
                # Checking name for the same letters only
                for i in range(len(repeat_numbers)):
                    if repeat_numbers[splited[i]] == len(value):
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
        elif name == 'addressId':
            if type(value) != int:
                raise TypeError('wrong Address id')
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
        if type(other) == Customer:
            if self.id == other.id:
                return True
            else:
                return False
        else:
            return False


class CustomerRepositoryFactory:
    def __init__(self):
        self._lastCreatedId = 0
        self._customers = []

    def __str__(self):
        if len(self._customers) != 0:
            out = ''
            for customer in self._customers:
                out = out + str(customer)
        else:
            out = '\nThere are no customers here\n'
        return out

    def __repr__(self):
        return str(self)

    # ##### Factory methods #####
    def getCustomer(self, firstName, lastName, addressId):
        obj = Customer(firstName, lastName, addressId)
        self._lastCreatedId += 1
        obj.id = self._lastCreatedId
        self._customers.append(obj)
        return obj

    def get_last_id(self):
        return f"\n{'-'*10}\n" + 'Last created object id: ' + str(self._lastCreatedId) + f"\n{'-'*10}\n"

    # ##### Repository methods #####
    def all(self):
        return self._customers.copy()

    def save(self, customer):
        # Type verify
        if type(customer) != Customer:
            raise TypeError('the entity should only be Customer type')
        # Id verify
        if len(self._customers) != 0:
            for c in self._customers:
                if customer == c:
                    raise AttributeError(
                        'a Customer object with this id already exists')
        self._customers.append(customer)

    def save_many(self, customers_list):
        # checking customers_list type
        if type(customers_list) != list:
            raise TypeError('customers you want save should be in the list')
        # checking object quantity
        if len(customers_list) in [0, 1]:
            l = len(customers_list)
            raise ValueError(f'at least 2 objects can be saved, not {l}')
        # checking objects type
        for i in range(len(customers_list)):
            if type(customers_list[i]) != Customer:
                raise TypeError(f'object with index {i} is not a Customer type')
        # checking objects id's
        for customer in customers_list:
            for c in self._customers:
                if customer.id == c.id:
                    raise AttributeError(
                        'a Customers object with this id already exists')
        self._customers.extend(customers_list)

    def overwrite(self, customers_list):
        # checking customers_list type
        if type(customers_list) != list:
            raise TypeError('customers you want overwrite should be in the list')
        # checking objects type
        for i in range(len(customers_list)):
            if type(customers_list[i]) != Customer:
                raise TypeError(f'object with index {i} is not a Customer type')
        # checking objects id's
        for customer in customers_list:
            for c in self._customers:
                if customer.id == c.id:
                    raise AttributeError(
                        'a Customer object with this id already exists')
        self._customers = customers_list

    def findById(self, id_, showMode=True):
        if type(id_) != int:
            raise TypeError('id must be int type')
        for customer in self._customers:
            if customer.id == id_:
                if showMode:
                    return f"\n{'-'*10}\n" + f'Customer found by id [{id_}]:' + str(customer) + f"\n{'-'*10}\n"
                else:
                    return customer
        if showMode:
            return f"\n{'-'*10}\n" + f'Customer found by id [{id_}]:' + '\n\nNothing was found' + f"\n{'-'*10}\n"

    def deleteById(self, id_):
        if type(id_) != int:
            raise TypeError('id must be int type')
        for customer in self._customers:
            if id_ == customer.id:
                self._customers.remove(customer)

    def findByFirstName(self, firstName, showMode=True):
        if type(firstName) != str:
            raise TypeError('first name must be str type')
        # With a incomplete match with the first name
        found = []
        for customer in self._customers:
            if firstName in customer.firstName:
                found.append(customer)
        if len(found) != 0:
            if showMode:
                out = ''
                for c in found:
                    out = out + str(c)
                return f"\n{'-'*10}\n" + f'Customers found by first name \"{firstName}\":' + out + f"\n{'-'*10}\n"
            else:
                return found
        # With a complete match with the first name
        for customer in self._customers:
            if customer.firstName == firstName:
                if showMode:
                    return f"\n{'-'*10}\n" + f'Customer found with first name \"{firstName}\":' + str(customer) + f"\n{'-'*10}\n"
                else:
                    return found
        if showMode:
            return f"\n{'-'*10}\n" + f'Customer found with first name \"{firstName}\":' + '\n\nNothing was found' + f"\n{'-'*10}\n"
        else:
            return found

    def findByLastName(self, lastName, showMode=True):
        if type(lastName) != str:
            raise TypeError('last name must be str type')
        # With a incomplete match with the last name
        found = []
        for customer in self._customers:
            if lastName in customer.lastName:
                found.append(customer)
        if len(found) != 0:
            out = ''
            for c in found:
                out = out + str(c)
            if showMode:
                return f"\n{'-'*10}\n" + f'Customers found by last name \"{lastName}\":' + out + f"\n{'-'*10}\n"
            else:
                return found
        # With a complete match with the last name
        for customer in self._customers:
            if customer.lastName == lastName:
                if showMode:
                    return f"\n{'-'*10}\n" + f'Customer found with last name \"{lastName}\":' + str(customer) + f"\n{'-'*10}\n"
                else:
                    return found
        if showMode:
            return f"\n{'-'*10}\n" + f'Customer found with last name \"{lastName}\":' + '\n\nNothing was found' + f"\n{'-'*10}\n"
        else:
            return found

    def findByAddressId(self, addressId, showMode=True):
        if type(addressId) != int:
            raise TypeError('address id must be int type')
        # search
        found = []
        for customer in self._customers:
            if customer.addressId == addressId:
                found.append(customer)
        # output
        if showMode:
            if len(found) == 0:
                return f"\n{'-'*10}\n" + f'Customers found by address id [{addressId}]:' + f'\n\nNothing was found' + f"\n{'-'*10}\n"
            else:
                out = ''
                for customer in found:
                    out = out + str(customer)
                return f"\n{'-'*10}\n" + f'Customers found by address id [{addressId}]:' + out + f"\n{'-'*10}\n"
        else:
            return found
