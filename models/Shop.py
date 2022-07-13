from db.templates import *


class Shop(Model):
    def __init__(self, id_, working_hours, address_id):
        self.id = id_
        self.inDB = False
        self.working_hours = working_hours
        self.address_id = address_id

    def __str__(self):
        title = f"--- Shop ---"
        id = f"Id: {self.id}"
        inDB = f'In DB: {self.inDB}'
        working_hours = f'Working hours: {self.working_hours}'
        address_id = f'Address id: {self.address_id}'
        return f'\n\n{title}\n{id}\n{inDB}\n{working_hours}\n{address_id}\n\n'

    def __repr__(self):
        return f'<<{[self.id, self.inDB, self.working_hours, self.address_id]}>>'

    def __setattr__(self, name, value):
        if name == 'id':
            if self.inDB == False:
                if type(value) != int: raise TypeError('id must have an int value')
        elif name == 'inDB':
            if value not in (True, False):
                raise TypeError('value for inDB attribute must be True or False only')
        elif name == 'working_hours':
            # Checking attribute type
            if type(value) != list: raise TypeError('working_hours must be list type')
            # Check working_hours list lenght
            if len(value) != 7:
                raise TypeError(
                    'the working_hours list should contain seven lists for 7 days of the week')
            # Checking lists in the working_hours list
            for i in range(len(value)):
                # Checking  type
                if type(value[i]) != list:
                    raise TypeError(f'object with index {i} in working_hours not is list')
                # Checking length
                if len(value[i]) != 2:
                    raise ValueError(
                        f'list with index {i} contain {len(value[i])} objects, not 2 (start work time, end work time)')
                # Checking values in the working_hours lists
                start_work, end_work = '', ''
                for v in range(len(value[i])):
                    # Checking type
                    if type(value[i][v]) != str:
                        raise TypeError(f'list with index {i} in working_hours contain not str type object with index {v}')
                    wrong_value = f'value with index {v} in list with index {i}'

                    # Checking str lenght
                    if len(value[i][v]) != 5: raise ValueError(f'{wrong_value} not contain 5 characters')

                    # Checking format
                    spl = value[i][v].split(':')
                    if len(spl) != 2: raise ValueError(f'{wrong_value} must be in correct format (00:00)')
                    if spl[0].isnumeric() == False: raise ValueError(f'{wrong_value} contain not numeric hours value')
                    if spl[1].isnumeric() == False: raise ValueError(f'{wrong_value} contain not numeric minutes value')
                    spl = [int(spl[0]), int(spl[1])]
                    if len(spl[0]) < 0: raise ValueError(f'{wrong_value} has negative hours value')
                    if len(spl[0]) > 23: raise ValueError(f'{wrong_value} has hours value more then 23')
                    if len(spl[1]) < 0: raise ValueError(f'{wrong_value} has negative minutes value')
                    if len(spl[1]) > 59: raise ValueError(f'{wrong_value} has minutes value more then 59')

                    # Start work and end work time definition
                    if v == 0: start_work = value[i][v]
                    elif v == 1: end_work = value[i][v]
                
                # Checking if end work > start work time value
                times_spls = [[int(v) for v in var.split(':')] for var in (start_work, end_work)]
                if times_spls[0][0] >= times_spls[1][0] and times_spls[0][1] >= times_spls[1][1]:
                    raise ValueError('start work time must be lesser then end work time')
                
                # Appending start work and end work time definition
                times_defs = [[str(times_spls[0][time_num] - times_spls[1][time_num]) if \
                    times_spls[0][time_num] - times_spls[1][time_num] > 9 else \
                    f'0{times_spls[0][time_num] - times_spls[1][time_num]}'] for time_num in range(2)]
                value[i].append(f'{times_defs[0]}:{times_defs[1]}')
        elif name == 'address_id':
            if type(value) != int:
                raise TypeError('address_id must be int type')
        object.__setattr__(self, name, value)

    def __eq__(self, other): return self.id == other.id if type(other) == Shop else False


class ShopRepositoryFactory(ModelRepositoryFactory):
    def __init__(self, pgds):
        self.pgds = pgds

    def __str__(self):
        data = self.pgds.query('SELECT * FROM shops')
        if len(data) != 0:
            shops = []
            for row in data:
                working_hours = row[1]
                for r in working_hours:
                    r.pop(2)
                s = self.get_shop(row[0], working_hours, row[2])
                s.inDB = True
                shops.append(s)
            out = ''.join(shops)
        else:
            out = '\nNo shops here\n'
        return out

    def __repr__(self): return str(self.pgds.query('SELECT * FROM shops'))

    # ##### Factory methods #####
    def get_shop(self, id_, working_hours, address_id): return Shop(id_, working_hours, address_id)

    # ##### Repository methods #####
    def all(self):
        data = self.pgds.query('SELECT * FROM shops')
        shops = []
        if len(data) > 0:
            for row in data:
                working_hours = row[1]
                for r in working_hours:
                    r.pop(2)
                s = self.get_shop(row[0], working_hours, row[2])
                s.inDB = True
                shops.append(s)
        return shops

    def save(self, shop):
        # Type verify
        if type(shop) != Shop: raise TypeError('the entity should be only Shop type')
        # Save object data
        wh = str(shop.working_hours).replace('[', '{').replace(']', '}')
        if shop.inDB == False:
            shop.id = self.pgds.query(f'INSERT INTO shops(working_hours, address_id)\
                VALUES ({wh}, {shop.address_id}) RETURNING id')[0][0]
            shop.inDB = True
        elif shop.inDB:
            self.pgds.query(f'UPDATE shops\
                SET working_hours = {wh}, address_id = {shop.address_id}, \
                WHERE id = {shop.id}')

    def save_many(self, *shops):
        # Checking object quantity
        l = len(shops)
        if l in [0, 1]:
            raise ValueError(f'at least 2 objects can be saved, not {l}')
        # Checking objects type
        for i in range(l):
            if type(shops[i]) != Shop:
                raise TypeError(f'object number {i+1} is not a Shop type')
        # Save objects data
        [self.save(shop) for shop in shops]

    def find_by_id(self, id_):
        if type(id_) != int: raise TypeError('id must be int')
        data = self.pgds.query(f'SELECT * FROM shops WHERE id = {id_}')
        if len(data) > 0:
            wh = [[v[0], v[1]] for v in data[0][1]]
            s = self.get_shop(data[0][0], wh, data[0][2])
            s.inDB = True
            return s

    def delete_by_id(self, id_):
        if type(id_) != int: raise TypeError('id must be int value')
        self.pgds.query(f'DELETE FROM shops WHERE id = {id_}')
