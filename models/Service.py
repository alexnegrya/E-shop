from db.templates import *


class Service(Model):
    def __init__(self, id_, name, price, description=None):
        self.id = id_
        self.inDB = False
        self.name = name
        self.price = price
        self.description = description

    def __str__(self):
        title = f"--- Service \"{self.name}\" ---"
        id = f"Id: {self.id}"
        inDB = f'In DB: {self.inDB}'
        price = f'Price: {self.price}'
        return f'\n\n{title}\n{id}\n{inDB}\n{price}\n\n'

    def __repr__(self):
        return f'<<{[self.id, self.inDB, self.name, self.price]}>>'

    def __setattr__(self, name, value):
        if name == 'id':
            if self.inDB == False:
                if type(value) != int:
                    raise TypeError('id must have an int value')
        elif name == 'inDB':
            if value in (True, False):
                object.__setattr__(self, name, value)
            else:
                raise TypeError(
                    'value for inDB attribute must be True or False only')
        elif name in ('name', 'description'):
            if type(value) != str:
                raise TypeError('value must be a string')
            elif value == '':
                raise NameError('value cannot be an empty string')
            else:
                # Spliting by letters
                splited = []
                for i in range(len(value)):
                    splited.append(value[i])
                # Checking for letters repition
                repeated_numbers = {}
                for i in range(len(splited)):
                    if splited[i] not in repeated_numbers:
                        repeated_numbers[splited[i]] = 1
                    else:
                        repeated_numbers[splited[i]] += 1
                # Checking for the same letters only
                for i in range(len(repeated_numbers)):
                    if repeated_numbers[splited[i]] == len(value):
                        raise NameError(
                            'the str value contains only the same letters')
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

    def __eq__(self, other): return self.id == other.id if type(other) == Service else False


class ServiceRepositoryFactory(ModelRepositoryFactory):
    def __init__(self, pgds):
        self.pgds = pgds

        from .Money import MoneyRepositoryFactory
        self.mrf = MoneyRepositoryFactory(self.pgds)

    def __str__(self):
        data = self.pgds.query('SELECT * FROM services')
        if len(data) != 0:
            services = []
            for row in data:
                s = self.get_service(row[0], row[1], self.mrf.find_by_id(row[3]), row[2])
                s.inDB = True
                services.append(s)
            out = ''
            for service in services:
                out = out + str(service)
        else:
            out = '\nNo services here\n'
        return out

    def __repr__(self):
        return str(self.pgds.query('SELECT * FROM services'))

    # ##### Factory methods #####
    def get_service(self, id_, name, price, description='null'):
        return Service(id_, name, price, description)

    # ##### Repository methods #####
    def all(self):
        data = self.pgds.query('SELECT * FROM services')
        if len(data) > 0:
            services = []
            for row in data:
                s = self.get_service(row[0], row[1], self.mrf.find_by_id(row[3]), row[2])
                s.inDB = True
                services.append(s)
            return services
        else:
            return []

    def save(self, service):
        # Type verify
        if type(service) != Service: raise TypeError('the entity should only be Service type')
        # Save object data
        description = "'" + service.description + "'" if service.description != None else "null"
        if service.inDB == False:
            service.id = self.pgds.query(f'INSERT INTO services(name, description, price_id)\
                VALUES (\'{service.name}\', {description}, {service.price.id})\
                RETURNING id')[0][0]
            service.inDB = True
        elif service.inDB:
            self.pgds.query(f'UPDATE services\
                SET name = \'{service.name}\', description = {description}, \
                price_id = {service.price.id} WHERE id = {service.id}')

    def save_many(self, *services):
        # Checking object quantity
        l = len(services)
        if l in [0, 1]: raise ValueError(f'at least 2 objects can be saved, not {l}')
        # Checking objects type
        for i in range(l):
            if type(services[i]) != Service:
                raise TypeError(f'object number {i+1} is not a Service type')
        # Save objects data
        [self.save(service) for service in services]

    def find_by_id(self, id_):
        if type(id_) != int: raise TypeError('id must be int type')
        data = self.pgds.query(f'SELECT * FROM services WHERE id = {id_}')
        if len(data) > 0:
            s = self.get_service(data[0][0], data[0][1], self.mrf.find_by_id(data[0][3]), data[0][2])
            s.inDB = True
            return s

    def delete_by_id(self, id_):
        if type(id_) != int: raise TypeError('id must be int type')
        self.pgds.query(f'DELETE FROM services WHERE id = {id_}')
