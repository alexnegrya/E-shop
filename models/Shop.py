class Shop:
    def __init__(self, id_, workingHours, addressId):
        self.id = id_
        self.inDB = False
        self.workingHours = workingHours
        self.addressId = addressId

    def __str__(self):
        title = f"--- Shop ---"
        id = f"Id: {self.id}"
        inDB = f'In DB: {self.inDB}'
        workingHours = f'Working hours: {self.workingHours}'
        addressId = f'Address id: {self.addressId}'
        return f'\n\n{title}\n{id}\n{inDB}\n{workingHours}\n{addressId}\n\n'

    def __repr__(self):
        return f'<<{[self.id, self.inDB, self.workingHours, self.addressId]}>>'

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
                raise TypeError(
                    'value for inDB attribute must be True or False only')
        elif name == 'workingHours':
            # Checking attribute type
            if type(value) != list:
                raise TypeError('workingHours must be list type')
            # Check workingHours list lenght
            if len(value) != 7:
                raise TypeError(
                    'the workingHours list should contain seven lists for 7 days of the week')
            # Checking lists in the workingHours list
            for i in range(len(value)):
                # Checking  type
                if type(value[i]) != list:
                    raise TypeError(f'object with index {i} in workingHours not is list')
                # Checking length
                if len(value[i]) != 2:
                    raise ValueError(
                        f'list with index {i} contain {len(value[i])} objects, not 2 (start work time, end work time)')
                # Checking values in the workingHours lists
                startWork = ''
                endWork = ''
                for v in range(len(value[i])):
                    # Checking type
                    if type(value[i][v]) != str:
                        raise TypeError(
                            f'list with index {i} in workingHours contain not str type object with index {v}')
                    wrongValue = f'value with index {v} in list with index {i}'
                    # Checking str lenght
                    if len(value[i][v]) != 5:
                        raise ValueError(
                            f'{wrongValue} not contain 5 characters')
                    # Checking format
                    spl = value[i][v].split(':')
                    if len(spl) != 2:
                        raise ValueError(
                            f'{wrongValue} must be in correct format (00:00)')
                    if spl[0].isnumeric() == False:
                        raise ValueError(f'{wrongValue} contain not numeric hours value')
                    if spl[1].isnumeric() == False:
                        raise ValueError(f'{wrongValue} contain not numeric minutes value')
                    spl = [int(spl[0]), int(spl[1])]
                    if len(spl[0]) < 0:
                        raise ValueError(f'{wrongValue} has negative hours value')
                    if len(spl[0]) > 23:
                        raise ValueError(f'{wrongValue} has hours value more then 23')
                    if len(spl[1]) < 0:
                        raise ValueError(f'{wrongValue} has negative minutes value')
                    if len(spl[1]) > 59:
                        raise ValueError(f'{wrongValue} has minutes value more then 59')
                    # Start work and end work time definition
                    if v == 0:
                        startWork = value[i][v]
                    elif v == 1:
                        endWork = value[i][v]
                # Checking if end work > start work time value
                startSpl = startWork.split(':')
                startSpl = [int(v) for v in startSpl]
                endSpl = endWork.split(':')
                endSpl = [int(v) for v in endSpl]
                if startSpl[0] >= endSpl[0] and startSpl[1] >= endSpl[1]:
                    raise ValueError('start work time must be lesser then end work time')
                # Appending start work and end work time definition
                hoursDef = endSpl[0] - startSpl[0]
                minutesDef = endSpl[1] - startSpl[1]
                for Def in (hoursDef, minutesDef):
                    if Def > 9:
                        Def = str(hoursDef)
                    else:
                        Def = f'0{hoursDef}'
                value[i].append(f'{hoursDef}:{minutesDef}')
            object.__setattr__(self, name, value)
        elif name == 'addressId':
            if type(value) != int:
                raise TypeError('addressId must be int type')
            else:
                object.__setattr__(self, name, value)
        else:
            object.__setattr__(self, name, value)

    def __eq__(self, other):
        if type(other) == Shop:
            if self.id == other.id:
                return True
            else:
                return False


class ShopRepositoryFactory:
    def __init__(self, pgds):
        self.pgds = pgds

    def __str__(self):
        data = self.pgds.query('SELECT * FROM shops')
        if len(data) != 0:
            shops = []
            for row in data:
                workingHours = row[1]
                for r in workingHours:
                    r.pop(2)
                s = self.getShop(row[0], workingHours, row[2])
                s.inDB = True
                shops.append(s)
            out = ''
            for shop in shops:
                out = out + str(shop)
        else:
            out = '\nNo shops here\n'
        return out

    def __repr__(self):
        return str(self.pgds.query('SELECT * FROM shops'))

    # ##### Factory methods #####
    def getShop(self, id_, workingHours, addressId):
        return Shop(id_, workingHours, addressId)

    # ##### Repository methods #####
    def all(self):
        data = self.pgds.query('SELECT * FROM shops')
        if len(data) > 0:
            shops = []
            for row in data:
                workingHours = row[1]
                for r in workingHours:
                    r.pop(2)
                s = self.getShop(row[0], workingHours, row[2])
                s.inDB = True
                shops.append(s)
            return shops
        else:
            return []

    def save(self, shop):
        # Type verify
        if type(shop) != Shop:
            raise TypeError('the entity should be only Shop type')
        # Save object data
        wh = str(shop.workingHours).replace('[', '{')
        wh = wh.replace(']', '}')
        if shop.inDB == False:
            shop.id = self.pgds.query(f'INSERT INTO shops(working_hours, address_id)\
                VALUES ({wh}, {shop.addressId}) RETURNING id')[0][0]
            shop.inDB = True
        elif shop.inDB:
            self.pgds.query(f'UPDATE shops\
                SET working_hours = {wh}, address_id = {shop.addressId}, \
                WHERE id = {shop.id}')

    def save_many(self, *shops):
        # Checking object quantity
        l = len(shops)
        if l in [0, 1]:
            raise ValueError(f'at least 2 objects can be saved, not {l}')
        # Checking objects type
        for i in range(len(shops)):
            if type(shops[i]) != Shop:
                raise TypeError(f'object number {i+1} is not a Shop type')
        # Save objects data
        for shop in shops:
            wh = str(shop.workingHours).replace('[', '{')
            wh = wh.replace(']', '}')
            if shop.inDB == False:
                shop.id = self.pgds.query(f'INSERT INTO shops(working_hours, address_id)\
                    VALUES ({wh}, {shop.addressId}) RETURNING id')[0][0]
                shop.inDB = True
            elif shop.inDB:
                self.pgds.query(f'UPDATE shops\
                    SET working_hours = {wh}, address_id = {shop.addressId}, \
                    WHERE id = {shop.id}')

    def findById(self, id_):
        # Checking type
        if type(id_) != int:
            raise TypeError('id must be int')
        # Search and return
        data = self.pgds.query(f'SELECT * FROM shops WHERE id = {id_}')
        if len(data) > 0:
            wh = [[v[0], v[1]] for v in data[0][1]]
            s = self.getShop(data[0][0], wh, data[0][2])
            s.inDB = True
            return s

    def deleteById(self, id_):
        # Checking type
        if type(id_) != int:
            raise TypeError('id must be int value')
        # Delete data
        self.pgds.query(f'DELETE FROM shops WHERE id = {id_}')
