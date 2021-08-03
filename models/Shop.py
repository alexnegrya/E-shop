class Shop:
    __ids = []

    def __init__(self, workingHours, addressId):
        self.id = self.__get_id()
        self.workingHours = workingHours
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
        title = f"--- Shop ---"
        id = f"Id: {self.id}"
        workingHours = f'Working hours: {self.workingHours}'
        addressId = f'Address id: {self.addressId}'
        out = f'\n\n{title}\n{id}\n{workingHours}\n{addressId}\n\n'
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
        elif name == 'workingHours':
            # Check attribute type
            if type(value) != list:
                raise TypeError('workingHours must be list type')
            # Check objects in the list
            for v in value:
                # check type
                if type(v) != int:
                    raise TypeError('values in workingHours list must be int type')
                # check value
                if v < 0 or v > 24:
                    raise ValueError(
                        'values in workingHours list must be in int range 0-24')
            # Check workingHours list lenght
            if len(value) != 7:
                raise TypeError(
                    'the workingHours list should contain seven values for 7 days of the week')
            # Create dict with days and working hours
            wh = {}
            days = ['Monday', 'Tuesday', 'Wednesday',
                'Thursday', 'Friday', 'Saturday', 'Sunday']
            for i in range(len(value)):
                wh[days[i]] = value[i]
            value = wh
            object.__setattr__(self, name, value)
        elif name == 'addressId':
            if type(value) != int:
                raise TypeError('addressId must be int type')
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
        if type(other) == Shop:
            if self.id == other.id:
                return True
            else:
                return False


class ShopRepositoryFactory:
    __days = ['Monday', 'Tuesday', 'Wednesday',
        'Thursday', 'Friday', 'Saturday', 'Sunday']

    def __init__(self):
        self._lastCreatedId = 0
        self._shops = []

    def __str__(self):
        if len(self._shops) != 0:
            out = ''
            for shop in self._shops:
                out = out + str(shop)
        else:
            out = '\nThere are no shops here\n'
        return out

    def __repr__(self):
        return str(self)

    # ##### Factory methods #####
    def getShop(self, workingHours, addressId):
        obj = Shop(workingHours, addressId)
        self._lastCreatedId += 1
        obj.id = self._lastCreatedId
        self._shops.append(obj)
        return obj

    def get_last_id(self):
        return f"\n{'-'*10}\n" + 'Last created object id: ' + str(self._lastCreatedId) + f"\n{'-'*10}\n"

    # ##### Repository methods #####
    def all(self):
        return tuple(self._shops)

    def save(self, shop):
        # Type verify
        if type(shop) != Shop:
            raise TypeError('the entity should be only Shop type')
        # Id verify
        if len(self._shops) != 0:
            for s in self._shops:
                if shop == s:
                    raise AttributeError(
                        'a Shop object with this id already exists')
        self._shops.append(shop)

    def save_many(self, shops_list):
        # checking shops_list type
        if type(shops_list) != list:
            raise TypeError('shops you want save should be in the list')
        # checking object quantity
        if len(shops_list) in [0, 1]:
            l = len(shops_list)
            raise ValueError(f'at least 2 objects can be saved, not {l}')
        # checking objects type
        for i in range(len(shops_list)):
            if type(shops_list[i]) != Shop:
                raise TypeError(
                    f'object with index {i} is not a Shop type')
        # checking objects id's
        for shop in shops_list:
            for s in self._shops:
                if shop == s:
                    raise AttributeError(
                        f'a Shop object with id {shop.id} already exists')
        self._shops.extend(shops_list)

    def save_many(self, shops_list):
        # checking shops_list type
        if type(shops_list) != list:
            raise TypeError('shops you want save should be in the list')
        # checking object quantity
        if len(shops_list) in [0, 1]:
            l = len(shops_list)
            raise ValueError(f'at least 2 objects can be saved, not {l}')
        # checking objects type
        for i in range(len(shops_list)):
            if type(shops_list[i]) != Shop:
                raise TypeError(
                    f'object with index {i} is not a Shop type')
        # checking objects id's
        for shop in shops_list:
            for s in self._shops:
                if shop == s:
                    raise AttributeError(
                        f'a Shop object with id {shop.id} already exists')
        self._shops = shops_list

    def findById(self, id_, showMode=True):
        for shop in self._shops:
            if shop.id == id_:
                if showMode:
                    return f"\n{'-'*10}\n" + f'Shop found by id [{id_}]:' + str(shop) + f"\n{'-'*10}\n"
                else:
                    return shop
        if showMode:
            return f"\n{'-'*10}\n" + f'Shop found by id [{id_}]:' + '\n\nNothing was found' + f"\n{'-'*10}\n"
        else:
            return shop

    def deleteById(self, id_):
        for shop in self._shops:
            if id_ == shop.id:
                self._shops.remove(shop)

    def getDays(self):
        return self.__days.copy()

    def findByWorkingHours(self, day, hours, showMode=True):
        # Check arguments types
        if type(day) != str:
            raise TypeError('day must be str type')
        if type(hours) != int:
            raise TypeError('hours must be int type')
        # Check day correctness
        correct = False
        for d in self.__days:
            if day == d:
                correct = True
        if not correct:
            raise TypeError('this day doesn\'t exist (call \"getDays\" method to get all days)')
        # Search
        found = []
        for shop in self._shops:
            for d in shop.workingHours:
                if d == day and shop.workingHours[day] == hours:
                    found.append(shop)
        # Output
        if len(found) != 0:
            if showMode:
                return f"\n{'-'*10}\nShops with {hours} working hours on {day} were found: \n{found}\n{'-'*10}"
            else:
                return found
        else:
            if showMode:
                return f"\n{'-'*10}\nShops with {hours} working hours on {day} were found: \nNothing was found\n{'-'*10}"
            else:
                return found

    def findByAddressId(self, addressId, showMode=True):
        # check type
        if type(addressId) != int:
            raise TypeError('addressId must be int type')
        # search
        found = []
        for shop in self._shops:
            if shop.addressId == addressId:
                found.append(shop)
        # output
        if len(found) != 0:
            if showMode:
                return f"\n{'-'*10}\nFound shops with address id [{addressId}]: \n{found}\n{'-'*10}"
            else:
                return found
        else:
            if showMode:
                return f"\n{'-'*10}\nFound shops with address id [{addressId}]: \nNothing was found\n{'-'*10}"
            else:
                return found
