class Customer:
    def __init__(self, id_, firstName, lastName, addressId):
        self.id = id_
        self.inDB = False
        self.firstName = firstName
        self.lastName = lastName
        self.addressId = addressId

    def __str__(self):
        title = f"--- Customer ---"
        id_ = f"Id: {self.id}"
        inDB = f'In DB: {self.inDB}'
        firstName = f'First name: {self.firstName}'
        lastName = f'Last name: {self.lastName}'
        addressId = f'Address id: {self.addressId}'
        out = f'\n\n{title}\n{id_}\n{inDB}\n{firstName}\n{lastName}\n{addressId}\n\n'
        return out

    def __repr__(self):
        return f'<<{[self.id, self.inDB, self.firstName, self.lastName, self.addressId]}>>'

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
        elif name in ('firstName', 'lastName'):
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
            from .Address import Address
            if type(value) not in [int, Address]:
                raise TypeError('wrong Address id')
            else:
                object.__setattr__(self, name, value)
        else:
            object.__setattr__(self, name, value)

    def __eq__(self, other):
        if type(other) == Customer:
            if self.id == other.id:
                return True
            else:
                return False
        else:
            return False


class CustomerRepositoryFactory:
    def __init__(self, pgds):
        self.pgds = pgds

    def __str__(self):
        data = self.pgds.query('SELECT id, full_name, address_id FROM clients')
        if len(data) != 0:
            customers = []
            for row in data:
                fullName = row[1].split(' ')
                firstName = fullName[0]
                lastName = fullName[1]
                c = self.getCustomer(row[0], firstName, lastName, row[2])
                c.inDB = True
                customers.append(c)
            out = ''
            for customer in customers:
                out = out + str(customer)
        else:
            out = '\nNo customers here\n'
        return out

    def __repr__(self):
        return str(self.pgds.query('SELECT * FROM clients'))

    # ##### Factory methods #####
    def getCustomer(self, id_, firstName, lastName, addressId):
        return Customer(id_, firstName, lastName, addressId)

    # ##### Repository methods #####
    def all(self):
        res = self.pgds.query('SELECT id, full_name, address_id FROM clients')
        if len(res) > 0:
            customers = []
            for row in res:
                fullName = row[1].split(' ')
                firstName = fullName[0]
                lastName = fullName[1]
                c = self.getCustomer(row[0], firstName, lastName, row[2])
                c.inDB = True
                customers.append(c)
            return customers
        else:
            return []

    def save(self, customer):
        # Type verify
        if type(customer) != Customer:
            raise TypeError('the entity should only be Customer type')
        # Save object data
        fullName = f'{customer.firstName} {customer.lastName}'
        if customer.inDB == False:
            customer.id = self.pgds.query(f'INSERT INTO clients(full_name, created, address_id)\
                VALUES (\'{fullName}\', now(), {customer.addressId})\
                RETURNING id')[0][0]
            customer.inDB = True
        elif customer.inDB:
            self.pgds.query(f'UPDATE clients\
                SET full_name = \'{fullName}\', updated = now(), \
                address_id = {customer.addressId} WHERE id = {customer.id}')

    def save_many(self, *customers):
        # Checking object quantity
        l = len(customers)
        if l in [0, 1]:
            raise ValueError(f'at least 2 objects can be saved, not {l}')
        # Checking objects type
        for i in range(len(customers)):
            if type(customers[i]) != Customer:
                raise TypeError(f'object number {i+1} is not a Customer type')
        # Save objects data
        for customer in customers:
            fullName = f'{customer.firstName} {customer.lastName}'
            if customer.inDB == False:
                customer.id = self.pgds.query(f'INSERT INTO clients(full_name, created, address_id)\
                    VALUES (\'{fullName}\', now(), {customer.addressId})\
                    RETURNING id')[0][0]
                customer.inDB = True
            elif customer.inDB:
                self.pgds.query(f'UPDATE clients\
                    SET full_name = \'{fullName}\', updated = now(), \
                    address_id = {customer.addressId} WHERE id = {customer.id}')

    def findById(self, id_):
        # Checking type
        if type(id_) != int:
            raise TypeError('id must be int type')
        # Search and return
        data = self.pgds.query(f'SELECT id, full_name, address_id FROM clients WHERE id = {id_}')
        if len(data) != 0:
            fullName = data[0][1].split(' ')
            firstName = fullName[0]
            lastName = fullName[1]
            c = self.getCustomer(data[0][0], firstName, lastName, data[0][2])
            c.inDB = True
            return c

    def deleteById(self, id_):
        # Checking type
        if type(id_) != int:
            raise TypeError('id must be int type')
        # Delete data
        self.pgds.query(f'DELETE FROM clients WHERE id = {id_}')
