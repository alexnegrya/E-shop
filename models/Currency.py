class Currency:
    __ids = []

    def __init__(self, code, nominal, rate):
        self.id = self.__get_id()
        self.code = code
        self.nominal = nominal
        self.rate = rate

    def __get_id(self):
        from random import randint
        ID = ''
        for v in range(randint(4, 6)):
            ID = ID + str(randint(0, 9))
        return int(ID)

    def __check_id(self, id_):
        if type(id_) == int:
            if id_ not in self.__ids:
                if id_ < 1 or id_ > 1000000:
                    raise ValueError('id must be in integer range 1-1000000')
                else:
                    return True
            else:
                raise ValueError('this id already occupied by other object')
        elif type(id_) == str:
            if id_ not in self.__ids:
                if int(id_) < 1 or int(id_) > 1000000:
                    raise ValueError('id must be in integer range 1-1000000')
                else:
                    return True
            else:
                raise ValueError('this id already occupied by other object')
        else:
            raise TypeError('unsupported id type')

    def __str__(self):
        title = f"--- Currency ---"
        id = f"Id: {self.id}"
        code = f'Code: {self.code}'
        nominal = f'Nominal: {self.nominal}'
        rate = f'Rate: {self.rate:.04f}'
        out = f'\n\n{title}\n{id}\n{code}\n{nominal}\n{rate}\n\n'
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
        elif name == 'code':
            if type(value) != str:
                raise TypeError('code must be a string')
            elif value == '':
                raise ValueError('code cannot be an empty string')
            elif len(value) != 3:
                raise ValueError('code must contain 3 letters')
            else:
                # Spliting code by letters
                splited = []
                for i in range(len(value)):
                    splited.append(value[i])
                # Checking code for letters repition
                repeated_letters = {}
                for i in range(len(splited)):
                    if splited[i] not in repeated_letters:
                        repeated_letters[splited[i]] = 1
                    else:
                        repeated_letters[splited[i]] += 1
                # Checking code for the same letters only
                for i in range(len(repeated_letters)):
                    if repeated_letters[splited[i]] == len(value):
                        raise NameError(
                            'the code contains only the same letters')
                # Cheking code for numbers
                for letter in splited:
                    try:
                        int(letter)
                        raise NameError(
                            'the code must not contain integer values')
                    except ValueError:
                        pass
                object.__setattr__(self, name, value)
        elif name == 'nominal':
            if type(value) != int:
                raise TypeError('nominal must be int type')
            else:
                object.__setattr__(self, name, value)
        elif name == 'rate':
            if type(value) != float:
                raise TypeError('rate must be float type')
            else:
                # checking numbers count after the dot
                charges = []
                append = False
                count = 0
                for number in f'{value:.04f}':
                    if append:
                        charges.append(int(number))
                        count += 1
                    if number == '.':
                        append = True
                if count != 4:
                    raise ValueError('rate must be with 4 numbers after the dot')
                else:
                    object.__setattr__(self, name, value)
        elif name == '__ids':
            raise AttributeError('changing this attribute is not allowed')
        else:
            object.__setattr__(self, name, value)

    def __getattr__(self, name):
        if name == 'id':
            object.__getattribute__(self, str(name))
        elif name == '__ids':
            return tuple(self.__ids)

    def __eq__(self, other):
        if type(other) == Currency:
            if self.id == other.id:
                return True
            else:
                return False


class CurrencyRepositoryFactory:
    def __init__(self):
        self._lastCreatedId = 0
        self._currencies = []

    def __str__(self):
        if len(self._currencies) != 0:
            out = ''
            for currency in self._currencies:
                out = out + str(currency)
        else:
            out = '\nThere are no currencies here\n'
        return out

    def __repr__(self):
        return str(self)

    # ##### Factory methods #####
    def getCurrency(self, code, nominal, rate):
        obj = Currency(code, nominal, rate)
        self._lastCreatedId += 1
        obj.id = self._lastCreatedId
        self._currencies.append(obj)
        return obj

    def get_last_id(self):
        return f"\n{'-'*10}\n" + 'Last created object id: ' + str(self._lastCreatedId) + f"\n{'-'*10}\n"

    # ##### Repository methods #####
    def all(self):
        return tuple(self._currencies)

    def save(self, currency):
        # Type verify
        if type(currency) != Currency:
            raise TypeError('the entity should be only Currency type')
        # Id verify
        if len(self._currencies) != 0:
            for c in self._currencies:
                if currency == c:
                    raise AttributeError(
                        'a Currency object with this id already exists')
        self._currencies.append(currency)

    def save_many(self, currencies_list):
        # checking currencies_list type
        if type(currencies_list) != list:
            raise TypeError('currencies you want save should be in the list')
        # checking object quantity
        if len(currencies_list) in [0, 1]:
            l = len(currencies_list)
            raise ValueError(f'at least 2 objects can be saved, not {l}')
        # checking objects type
        for i in range(len(currencies_list)):
            if type(currencies_list[i]) != Currency:
                raise TypeError(
                    f'object with index {i} is not a Currency type')
        # checking objects id's
        for currency in currencies_list:
            for c in self._currencies:
                if currency.id == c.id:
                    raise AttributeError(
                        'a Currency object with this id already exists')
        self._currencies.extend(currencies_list)

    def overwrite(self, currencies_list):
        # checking currencies_list type
        if type(currencies_list) != list:
            raise TypeError(
                'currencies you want overwrite should be in the list')
        # checking objects type
        for i in range(len(currencies_list)):
            if type(currencies_list[i]) != Currency:
                raise TypeError(
                    f'object with index {i} is not a Currency type')
        # checking objects id's
        for currency in currencies_list:
            for c in self._currencies:
                if currency.id == c.id:
                    raise AttributeError(
                        'a Currency object with this id already exists')
        self._currencies = currencies_list

    def findById(self, id_, showMode=True):
        # check type
        if type(id_) not in [int, str]:
            raise TypeError('id must be int or str type')
        # check str
        try:
            int(id_)
        except ValueError:
            error = True
        else:
            error = False
        if error:
            raise ValueError('str id must contain only numbers')
        # search and output
        if type(id_) == str:
            f = f'\"{id_}\"'
        else:
            f = f'[{id_}]'
        for currency in self._currencies:
            if currency.id == id_:
                if showMode:
                    return f"\n{'-'*10}\n" + f'Currency found by id {f}:' + str(currency) + f"\n{'-'*10}\n"
                else:
                    return currency
        if showMode:
            return f"\n{'-'*10}\n" + f'Currency found by id {f}:' + '\n\nNothing was found' + f"\n{'-'*10}\n"
        else:
            return currency

    def findByCode(self, code, showMode=True):
        # check code
        if type(code) != str:
            raise TypeError('code must be str type')
        # With a incomplete match with the code
        found = []
        for currency in self._currencies:
            if code in currency.code:
                found.append(currency)
        if len(found) != 0:
            if showMode:
                out = ''
                for c in found:
                    out = out + str(c)
                return f"\n{'-'*10}\n" + f'Currencies found by code \"{code}\":' + out + f"\n{'-'*10}\n"
            else:
                return found
        # With a complete match with the code
        for currency in self._currencies:
            if currency.code == code:
                if showMode:
                    return f"\n{'-'*10}\n" + f'Currency found with code \"{code}\":' + str(currency) + f"\n{'-'*10}\n"
                else:
                    return found
        if showMode:
            return f"\n{'-'*10}\n" + f'Currency found with code \"{code}\":' + '\n\nNothing was found' + f"\n{'-'*10}\n"
        else:
            return found

    def findByNominal(self, nominal, showMode=True):
        # check type
        if type(nominal) != int:
            raise TypeError('nominal must be int type')
        # search
        found = []
        for currency in self._currencies:
            if currency.nominal == nominal:
                found.append(currency)
        found.reverse()
        # output
        if len(found) != 0:
            if showMode:
                return f"\n{'-'*10}\nFound currencies with nominal [{nominal}]: \n{found}\n{'-'*10}"
            else:
                return found
        else:
            if showMode:
                return f"\n{'-'*10}\nFound currencies with nominal [{nominal}]: \nNothing was found\n{'-'*10}"
            else:
                return found

    def findByNominalRange(self, nominalMin, nominalMax, showMode=True):
        # check type
        for nominal in [nominalMin, nominalMax]:
            if type(nominal) != int:
                raise TypeError('nominal ranges must be int type')
        # search
        found = []
        for currency in self._currencies:
            if currency.nominal >= nominalMin\
                    and currency.nominal <= nominalMax:
                found.append(currency)
        found.reverse()
        # output
        if len(found) != 0:
            if showMode:
                return f"\n{'-'*10}\nFound currencies in nominal range [{nominalMin}-{nominalMax}]: \n{found}\n{'-'*10}"
            else:
                return found
        else:
            if showMode:
                return f"\n{'-'*10}\nFound currencies in nominal range [{nominalMin}-{nominalMax}]: \nNothing was found\n{'-'*10}"
            else:
                return found

    def findByRate(self, rate, showMode=True):
        # check type
        if type(rate) not in [int, float]:
            raise TypeError('rate must be int or float type')
        # search
        found = []
        for currency in self._currencies:
            if type(rate) == int:
                if currency.rate >= rate and currency.rate < (rate + 1):
                    found.append(currency)
            else:
                if currency.rate >= rate and currency.rate <= (int(rate) + 1):
                    found.append(currency)
        found.reverse()
        # output
        if len(found) != 0:
            if showMode:
                return f"\n{'-'*10}\nFound currencies with rate [{rate}]: \n{found}\n{'-'*10}"
            else:
                return found
        else:
            if showMode:
                return f"\n{'-'*10}\nFound currencies with rate [{rate}]: \nNothing was found\n{'-'*10}"
            else:
                return found

    def findByRateRange(self, rateMin, rateMax, showMode=True):
        # check type
        for rate in [rateMin, rateMax]:
            if type(rate) not in [int, float]:
                raise TypeError('rate ranges must be int or float type')
        # search
        found = []
        for currency in self._currencies:
            if currency.rate >= rateMin and currency.rate <= rateMax:
                found.append(currency)
        found.reverse()
        # output
        if len(found) != 0:
            if showMode:
                return f"\n{'-'*10}\nFound currencies in rate range [{rateMin}-{rateMax}]: \n{found}\n{'-'*10}"
            else:
                return found
        else:
            if showMode:
                return f"\n{'-'*10}\nFound currencies in rate range [{rateMin}-{rateMax}]: \nNothing was found\n{'-'*10}"
            else:
                return found

    def deleteById(self, id_):
        # check type
        if type(id_) not in [int, str]:
            raise TypeError('id must be int or str type')
        # check str
        try:
            int(id_)
        except ValueError:
            error = True
        else:
            error = False
        if error:
            raise ValueError('str id must contain only numbers')
        # search and remove
        for currency in self._currencies:
            if id_ == currency.id:
                self._currencies.remove(currency)


class CurrencyService:
    def getCurrencies(self):
        # Getting current date
        from datetime import date
        d = str(date.today()).split('-')
        d.reverse()
        current_date = ''
        for n in range(len(d)):
            if n == 0:
                current_date = current_date + d[n]
            else:
                current_date = current_date + '.' + d[n]
        # Parcing currencies
        import requests
        url = f'https://www.bnm.md/ru/official_exchange_rates?get_xml=1&date={current_date}'
        res = requests.get(url)
        data = res.text
        # Getting data from xml
        from xml.etree import ElementTree
        root = ElementTree.fromstring(data)
        out = []
        for i in range(len(root)):
            c = Currency(root[i].find('CharCode').text, int(root[i].find('Nominal').text),
                float(root[i].find('Value').text))
            id_ = root[i].find('NumCode').text
            if int(id_) < 100:
                c.id = id_
            else:
                c.id = int(id_)
            out.append(c)
        return out
