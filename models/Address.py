class Address:
    __ids = []

    def __init__(self, country, city, street, number):
        self.id = self.__get_id()
        self.country = country
        self.city = city
        self.street = street
        self.number = number

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
        title = f"--- Address ---"
        id = f"Id: {self.id}"
        country = f'Country: {self.country}'
        city = f'City: {self.city}'
        street = f'Street: {self.street}'
        number = f'Street number: {self.number}'
        return f'\n\n{title}\n{id}\n{country}\n{city}\n{street}\n{number}\n\n'

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
        elif name in ['country', 'city', 'street']:
            if type(value) != str:
                raise TypeError('value must be a string')
            elif value == '':
                raise NameError('value cannot be an empty string')
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
                # Cheking name for numbers
                for letter in splited:
                    try:
                        int(letter)
                        raise NameError(
                            'the value must not contains integer values')
                    except ValueError:
                        pass
                # Checking name for the same letters only
                for i in range(len(repeated_numbers)):
                    if repeated_numbers[splited[i]] == len(value):
                        raise NameError(
                            'the value contains only the same letters')
                object.__setattr__(self, name, value)
        elif name == 'number':
            if type(value) != int and type(value) != str:
                raise TypeError('wrong number type')
            if type(value) == str:
                # Checking value for emptiness
                if value in ('', ' '):
                    raise ValueError('value must not be empty')
                # Spliting str by characters
                splited = []
                for i in range(len(value)):
                    splited.append(value[i])
                # Checking str for characters repition
                repeated_numbers = {}
                for i in range(len(splited)):
                    if splited[i] not in repeated_numbers:
                        repeated_numbers[splited[i]] = 1
                    else:
                        repeated_numbers[splited[i]] += 1
                # Checking str for the content of letters
                if value.isupper() or value.islower():
                    raise ValueError('value must not contains letters')
                object.__setattr__(self, name, value.strip())
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
        if type(other) == Address:
            if self.id == other.id:
                return True
            else:
                return False


class AddressRepositoryFactory:
    def __init__(self):
        self._lastCreatedId = 0
        self._addresses = []

    def __str__(self):
        if len(self._addresses) != 0:
            out = ''
            for address in self._addresses:
                out = out + str(address)
        else:
            out = '\nThere are no addresses here\n'
        return out

    def __repr__(self):
        return str(self)

    # ##### Factory methods #####
    def getAddress(self, country, city, street, number):
        obj = Address(country, city, street, number)
        self._lastCreatedId += 1
        obj.id = self._lastCreatedId
        self._addresses.append(obj)
        return obj

    def get_last_id(self):
        return f"\n{'-'*10}\n" + 'Last created object id: ' + str(self._lastCreatedId) + f"\n{'-'*10}\n"

    # ##### Repository methods #####
    def all(self):
        return self._addresses.copy()

    def save(self, address):
        # Type verify
        if type(address) != Address:
            raise TypeError('the entity should only be Address type')
        # Id verify
        if len(self._addresses) != 0:
            for a in self._addresses:
                if address == a:
                    raise AttributeError(
                        'a Address object with this id already exists')
        self._addresses.append(address)

    def save_many(self, addresses_list):
        # checking addresses_list type
        if type(addresses_list) != list:
            raise TypeError('addresses you want save should be in the list')
        # checking object quantity
        if len(addresses_list) in [0, 1]:
            l = len(addresses_list)
            raise ValueError(f'at least 2 objects can be saved, not {l}')
        # checking objects type
        for i in range(len(addresses_list)):
            if type(addresses_list[i]) != Address:
                raise TypeError(
                    f'object with index {i} is not a Address type')
        # checking objects id's
        for address in addresses_list:
            for a in self._addresses:
                if address.id == a.id:
                    raise AttributeError(
                        'a Address object with this id already exists')
        self._addresses.extend(addresses_list)

    def overwrite(self, addresses_list):
        # checking addresses_list type
        if type(addresses_list) != list:
            raise TypeError(
                'addresses you want overwrite should be in the list')
        # checking objects type
        for i in range(len(addresses_list)):
            if type(addresses_list[i]) != Address:
                raise TypeError(
                    f'object with index {i} is not a Address type')
        # checking objects id's
        for address in addresses_list:
            for a in self._addresses:
                if address.id == a.id:
                    raise AttributeError(
                        'a Address object with this id already exists')
        self._addresses = addresses_list

    def findById(self, id_, showMode=True):
        if type(id_) != int:
            raise TypeError('id must be int type')
        for address in self._addresses:
            if address.id == id_:
                if showMode:
                    return f"\n{'-'*10}\n" + f'address found by id [{id_}]:' + str(address) + f"\n{'-'*10}\n"
                else:
                    return address
        if showMode:
            return f"\n{'-'*10}\n" + f'address found by id [{id_}]:' + '\n\nNothing was found' + f"\n{'-'*10}\n"
        else:
            return address

    def deleteById(self, id_):
        if type(id_) != int:
            raise TypeError('id must be int type')
        for address in self._addresses:
            if id_ == address.id:
                self._addresses.remove(address)

    def findByCountry(self, country, showMode=True):
        if type(country) != str:
            raise TypeError('country must be str type')
        # With a incomplete match with the country
        found = []
        for address in self._addresses:
            if country in address.country:
                found.append(address)
        if len(found) != 0:
            if showMode:
                out = ''
                for a in found:
                    out = out + str(a)
                return f"\n{'-'*10}\n" + f'Addresses found by country keyword \"{country}\":' + out + f"\n{'-'*10}\n"
            else:
                return found
        # With a complete match with the country
        for address in self._addresses:
            if address.country == country:
                if showMode:
                    return f"\n{'-'*10}\n" + f'Found address with country \"{country}\":' + str(address) + f"\n{'-'*10}\n"
                else:
                    return found
        if showMode:
            return f"\n{'-'*10}\n" + f'Found address with country \"{country}\":' + '\n\nNothing was found' + f"\n{'-'*10}\n"
        else:
            return found

    def findByCity(self, city, showMode=True):
        if type(city) != str:
            raise TypeError('city must be str type')
        # With a incomplete match with the city
        found = []
        for address in self._addresses:
            if city in address.city:
                found.append(address)
        if len(found) != 0:
            if showMode:
                out = ''
                for a in found:
                    out = out + str(a)
                return f"\n{'-'*10}\n" + f'Addresses found by city keyword \"{city}\":' + out + f"\n{'-'*10}\n"
            else:
                return found
        # With a complete match with the city
        for address in self._addresses:
            if address.city == city:
                if showMode:
                    return f"\n{'-'*10}\n" + f'Found address with city \"{city}\":' + str(address) + f"\n{'-'*10}\n"
                else:
                    return found
        if showMode:
            return f"\n{'-'*10}\n" + f'Found address with city \"{city}\":' + '\n\nNothing was found' + f"\n{'-'*10}\n"
        else:
            return found
    
    def findByStreet(self, street, showMode=True):
        if type(street) != str:
            raise TypeError('street must be str type')
        # With a incomplete match with the street
        found = []
        for address in self._addresses:
            if street in address.street:
                found.append(address)
        if len(found) != 0:
            if showMode:
                out = ''
                for a in found:
                    out = out + str(a)
                return f"\n{'-'*10}\n" + f'Addresses found by street keyword \"{street}\":' + out + f"\n{'-'*10}\n"
            else:
                return found
        # With a complete match with the street
        for address in self._addresses:
            if address.street == street:
                if showMode:
                    return f"\n{'-'*10}\n" + f'Found address with street \"{street}\":' + str(address) + f"\n{'-'*10}\n"
                else:
                    return found
        if showMode:
            return f"\n{'-'*10}\n" + f'Found address with street \"{street}\":' + '\n\nNothing was found' + f"\n{'-'*10}\n"
        else:
            return found

    def findByNumber(self, number, showMode=True):
        if type(number) == int:
            # search
            found = []
            for address in self._addresses:
                if address.number == number:
                    found.append(address)
            # output
            if showMode:
                if len(found) == 0:
                    return f"\n{'-'*10}\n" + f'Addresses found by number [{number}]:' + f'\n\nNothing was found' + f"\n{'-'*10}\n"
                else:
                    out = ''
                    for address in found:
                        out = out + str(address)
                    return f"\n{'-'*10}\n" + f'Addresses found by number [{number}]:' + out + f"\n{'-'*10}\n"
            else:
                return found
        elif type(number) == str:
            # With a incomplete match with the number
            found = []
            for address in self._addresses:
                if number in address.number:
                    found.append(address)
            if len(found) != 0:
                if showMode:
                    out = ''
                    for a in found:
                        out = out + str(a)
                    return f"\n{'-'*10}\n" + f'Addresses found by street number keyword \"{number}\":' + out + f"\n{'-'*10}\n"
                else:
                    return found
            # With a complete match with the number
            for address in self._addresses:
                if address.number == number:
                    if showMode:
                        return f"\n{'-'*10}\n" + f'Found address with number \"{number}\":' + str(address) + f"\n{'-'*10}\n"
                    else:
                        return found
            if showMode:
                return f"\n{'-'*10}\n" + f'Found address with number \"{number}\":' + '\n\nNothing was found' + f"\n{'-'*10}\n"
            else:
                return found
        else:
            raise TypeError('unsupported number type')
