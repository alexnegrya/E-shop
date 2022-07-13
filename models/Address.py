from db.templates import *


class Address(Model):
    test_data = {
        'id': 1,
        'country': 'test',
        'city': 'test',
        'street': 'test',
        'number': '1/2'
    }

    def __init__(self, id_, country, city, street, number):
        self.inDB = False
        self.id = id_
        self.country = country
        self.city = city
        self.street = street
        self.number = number

    def __str__(self):
        title = f"--- Address ---"
        id = f"Id: {self.id}"
        inDB = f'In DB: {self.inDB}'
        country = f'Country: {self.country}'
        city = f'City: {self.city}'
        street = f'Street: {self.street}'
        number = f'Number: {self.number}'
        return f'{title}\n{id}\n{inDB}\n{country}\n{city}\n{street}\n{number}'

    def __repr__(self):
        return f'<<{[self.id, self.inDB, self.country, self.city, self.street, self.number]}>>'

    def __setattr__(self, name, value):
        if name == 'id':
            if self.inDB == False:
                if type(value) != int: raise TypeError('id must have an int value')
        elif name == 'inDB':
            if value not in (True, False):
                raise TypeError(
                    'value for inDB attribute must be True or False only')
        elif name in ('country', 'city', 'street'):
            if type(value) != str:
                raise TypeError('value must be a string')
            elif value == '':
                raise ValueError('value cannot be an empty string')
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
                        raise ValueError(
                            'the value contains only the same letters')
        elif name == 'number':
            if type(value) != int and type(value) != str:
                raise TypeError('wrong number type')
            if type(value) == str:
                # Checking str for the content of letters
                if value.isupper() or value.islower():
                    raise ValueError('value must not contain letters')
            value = value.strip()
        object.__setattr__(self, name, value)

    def __eq__(self, other): return self.id == other.id if type(other) == Address else False


class AddressRepositoryFactory(ModelRepositoryFactory):
    def __init__(self, pgds):
        self.pgds = pgds

    def __str__(self):
        addresses = self.pgds.query('SELECT * FROM addresses')
        if len(addresses) != 0:
            addrs = []
            for row in addresses:
                a = self.get_address(row[0], row[1], row[2], row[3], row[4])
                a.inDB = True
                addrs.append(a)
            out = ''
            for address in addrs:
                out = out + str(address)
        else:
            out = '\nNo addresses here\n'
        return out

    def __repr__(self):
        return str(self.pgds.query('SELECT * FROM addresses'))

    # ##### Factory methods #####
    def get_address(self, id_, country, city, street, number):
        return Address(id_, country, city, street, number)

    # ##### Repository methods #####
    def all(self):
        res = self.pgds.query('SELECT * FROM addresses')
        if len(res) > 0:
            addresses = []
            for row in res:
                a = self.get_address(row[0], row[1], row[2], row[3], row[4])
                a.inDB = True
                addresses.append(a)
            return addresses
        else:
            return []

    def save(self, address):
        # Type verify
        if type(address) != Address:
            raise TypeError('the entity should only be Address type')
        # Save object data
        if address.inDB == False:
            address.id = self.pgds.query(f'INSERT INTO addresses(country, city, street, number)\
                VALUES (\'{address.country}\', \'{address.city}\', \'{address.street}\', \'{address.number}\')\
                RETURNING id')[0][0]
            address.inDB = True
        elif address.inDB:
            self.pgds.query(f'UPDATE addresses\
                SET country = \'{address.country}\', city = \'{address.city}\', \
                street = \'{address.street}\', number = \'{address.number}\'\
                WHERE id = {address.id}')

    def save_many(self, *addresses):
        # Checking object quantity
        l = len(addresses)
        if l in [0, 1]:
            raise ValueError(f'at least 2 objects can be saved, not {l}')
        # Checking objects type
        for i in range(len(addresses)):
            if type(addresses[i]) != Address:
                raise TypeError(f'object number {i+1} is not a Address type')
        # Save objects data
        for address in addresses:
            if address.inDB == False:
                address.id = self.pgds.query(f'INSERT INTO addresses(country, city, street, number)\
                    VALUES (\'{address.country}\', \'{address.city}\', \'{address.street}\', \'{address.number}\')\
                    RETURNING id')[0][0]
                address.inDB = True
            elif address.inDB:
                self.pgds.query(f'UPDATE addresses\
                    SET country = \'{address.country}\', city = \'{address.city}\', \
                    street = \'{address.street}\', number = \'{address.number}\'\
                    WHERE id = {address.id}')

    def update(self, id_: int, **attrs):
        fields = list(attrs.keys())
        if all([key in Address.test_data for key in fields]):
            update_strings = [f"{attr} = " + (attrs[attr] if type(attrs[attr]) != str else f"'{attrs[attr]}'") for attr in fields]
            self.pgds.query(f'UPDATE addresses SET {", ".join(update_strings)} WHERE id = {id_}')
        else:
            raise ValueError('unknown attr(s) received')

    def find_by_id(self, id_):
        # Checking type
        if type(id_) != int:
            raise TypeError('id must be int type')
        # Search and return
        data = self.pgds.query(f'SELECT * FROM addresses WHERE id = {id_}')
        if len(data) > 0:
            a = self.get_address(data[0][0], data[0][1], data[0][2], data[0][3], data[0][4])
            a.inDB = True
            return a

    def delete_by_id(self, id_):
        # Checking type
        if type(id_) != int:
            raise TypeError('id must be int type')
        # Delete data
        self.pgds.query(f'DELETE FROM addresses WHERE id = {id_}')
