from db.templates import *
import re
from datetime import datetime


class Customer(Model):
    test_data = {
        'id': 1,
        'email': 'test@test.to',
        'first_name': 'test',
        'last_name': 'test',
        'password': 'test1234',
        'address_id': 1
    }

    def __init__(self, id_, email, first_name, last_name, password, address_id=None):
        self.inDB = False
        self.id = id_
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.address_id = address_id
        self.created = datetime.now()
        self.updated = None

    def __str__(self):
        title = f"--- Customer ---"
        id_ = f"Id: {self.id}"
        inDB = f'In DB: {self.inDB}'
        email = f'Email: {self.email}'
        first_name = f'First name: {self.first_name}'
        last_name = f'Last name: {self.last_name}'
        password = f'Password: {self.password[0] + "*" * len(self.password[1:-1]) + self.password[-1]}'
        address_id = f'Address id: {self.address_id}'
        out = f'{title}\n{id_}\n{inDB}\n{email}\n{first_name}\n{last_name}\n{password}\n{address_id}'
        return out

    def __repr__(self):
        return f'<<{[self.id, self.inDB, self.email, self.first_name, self.last_name, self.address_id]}>>'

    def __setattr__(self, name, value):
        if name == 'id':
            if self.inDB == False:
                if type(value) != int:
                    raise TypeError('id must have an int value')
        elif name == 'inDB':
            if type(value) != bool:
                raise TypeError('value for inDB attribute must be boolean')
        elif name == 'email':
            email_pattern = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
            if not re.search(email_pattern, value):
                raise ValueError('wrong email format')
        elif name in ('first_name', 'last_name'):
            if type(value) != str:
                raise TypeError('name must be a string')
            elif value == '':
                raise NameError('name cannot be an empty string')
            else:
                formated_name = name[0].upper() + name[1:].replace('_', ' ')
                splited = list(value)
                if ' ' in splited: raise ValueError(f'{formated_name} must not contains spaces')
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
                        raise NameError(f'{formated_name} contains only the same letters')
                # Cheking name for numbers
                for letter in splited:
                    try:
                        int(letter)
                        raise NameError(f'{formated_name} must not contain integer values')
                    except ValueError:
                        pass
        elif name == 'password':
            if len(value) < 8:
                raise ValueError('password length must be at least 8 characters')
        elif name == 'address_id':
            if value != None and type(value) != int:
                raise TypeError('wrong type of Address id')
        # if type(value) == str:
        #     if any(char in value for char in ('"', "'")):
        #         raise ValueError(f'{" ".join(name.split("_")).strip()} must not contains quotes')
        elif name in ('created', 'updated'):
            if type(value) != datetime: raise TypeError('created or updated must have datetime object value')
        self.__setattr__('updated', datetime.now())
        object.__setattr__(self, name, value)

    def __eq__(self, other): return self.id == other.id if type(other) == Customer else False


class CustomerRepositoryFactory(ModelRepositoryFactory):
    def __init__(self, pgds):
        self.pgds = pgds

    def __str__(self):
        customers = self.all()
        if len(customers) > 0:
            return ''.join(customers)
        else:
            return '\nNo customers here\n'

    def __repr__(self):
        return str(self.pgds.query('SELECT * FROM clients'))

    # ##### Factory methods #####
    def get_customer(self, id_, email, first_name, last_name, password, address_id=None):
        return Customer(id_, email, first_name, last_name, password, address_id)

    # ##### Repository methods #####
    def all(self):
        data = self.pgds.query('SELECT id, email, first_name, last_name, password, address_id FROM clients')
        if len(data) > 0:
            return [self.get_customer(row[0], row[1], row[2], row[3], row[4], row[5]) for row in data]
        return data

    def save(self, customer):
        if type(customer) != Customer: raise TypeError('the entity should only be Customer type')
        if customer.inDB == False:
            customer.id = self.pgds.query(f'INSERT INTO clients(email, first_name, last_name, password, created, address_id)\
                VALUES (\'{customer.email}\', \'{customer.first_name}\', \'{customer.last_name}\', \'{customer.password}\', now(), {customer.address_id})\
                RETURNING id')[0][0]
            customer.inDB = True
        elif customer.inDB:
            self.pgds.query(f'UPDATE clients\
                SET email = \'{customer.email}\', first_name = \'{customer.first_name}\', last_name = \'{customer.last_name}\', updated = now(), \
                password = \'{customer.password}\', address_id = {customer.address_id} WHERE id = {customer.id}')

    def save_many(self, *customers):
        if len(customers) in (0, 1): raise ValueError('at least 2 objects can be saved')
        if any([type(c) != Customer for c in customers]): raise TypeError('all objects must have Customer type')
        [self.save(c) for c in customers]

    def update(self, id_: int, **attrs):
        fields = list(attrs.keys())
        if all([key in Customer.test_data for key in fields]):
            update_strings = [f"{attr} = " + (attrs[attr] if type(attrs[attr]) != str else f"'{attrs[attr]}'") for attr in fields]
            self.pgds.query(f'UPDATE clients SET {", ".join(update_strings)} WHERE id = {id_}')
        else:
            raise ValueError('unknown attr(s) received')

    def find_by_id(self, id_):
        if type(id_) != int: raise TypeError('id must be int type')
        data = self.pgds.query(f'SELECT id, email, first_name, last_name, password, address_id FROM clients WHERE id = {id_}')
        if len(data) > 0:
            if len(data) == 1:
                c = self.get_customer(data[0][0], data[0][1], data[0][2], data[0][3], data[0][4], data[0][5])
                c.inDB = True
                return c
            elif len(data) > 1:
                raise ValueError(f'many objects with id {id_} exist')

    def find_by_data(self, id_=None, email=None, first_name=None, last_name=None, password=None, address_id=None) -> list:
        if all([value == None for value in list(locals().values())]):
            raise ValueError('At least one argument need be specified')
        wrap_str_to_quotes = lambda string: "'" + string + "'"
        args_dict = {k.strip('_'): v for k, v in locals().items() if v != None}
        [args_dict.pop(key) for key in ('self', 'wrap_str_to_quotes')]
        [self.get_customer(
            value if attr == 'id' else Customer.test_data['id'],
            value if attr == 'email' else Customer.test_data['email'],
            value if attr == 'first_name' else Customer.test_data['first_name'],
            value if attr == 'last_name' else Customer.test_data['last_name'],
            value if attr == 'password' else Customer.test_data['password'],
            value if attr == 'address_id' else Customer.test_data['address_id']
        ) for attr, value in args_dict.items()]
        data = self.pgds.query(f'''SELECT id, email, first_name, last_name, password, address_id FROM clients
            WHERE {" AND ".join([f"{arg} = {value if type(value) != str else wrap_str_to_quotes(value)}" if value != None else "" for arg, value in args_dict.items()])};''')
        customers = [self.get_customer(row[0], row[1], row[2], row[3], row[4], row[5]) for row in data]
        [setattr(c, 'inDB', True) for c in customers]
        return customers

    def delete_by_id(self, id_):
        if type(id_) != int: raise TypeError('id must be int type')
        self.pgds.query(f'DELETE FROM clients WHERE id = {id_}')
