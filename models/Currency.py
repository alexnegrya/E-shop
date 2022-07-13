from db.templates import *


class Currency(Model):
    def __init__(self, num_code, char_code, nominal, rate):
        self.inDB = False
        self.num_code = num_code
        self.char_code = char_code
        self.nominal = nominal
        self.rate = rate

    def __str__(self):
        title = f"--- Currency ---"
        inDB = f'In DB: {self.inDB}'
        num_code = f"num_code: {self.num_code}"
        char_code = f'char_code: {self.char_code}'
        nominal = f'Nominal: {self.nominal}'
        rate = f'Rate: {self.rate:.04f}'
        out = f'\n\n{title}\n{inDB}\n{num_code}\n{char_code}\n{nominal}\n{rate}\n\n'
        return out

    def __repr__(self):
        return f'<<[{self.inDB}, {self.num_code}, {self.char_code}, {self.nominal}, {self.rate:.04f}]>>'

    def __setattr__(self, name, value):
        if name == 'inDB':
            if value in (True, False):
                object.__setattr__(self, name, value)
            else:
                raise TypeError('value for inDB attribute must be True or False only')
        elif name == 'num_code':
            if type(value) != str:
                raise TypeError('value for num_code must be str type')
            elif len(value) != 3:
                raise ValueError('str must contain 3 characters')
            elif value.isnumeric() == False:
                raise ValueError('value must contain only numbers in str')
        elif name == 'char_code':
            if type(value) != str:
                raise TypeError('char_code must be a string')
            elif value == '':
                raise ValueError('char_code cannot be an empty string')
            elif len(value) != 3:
                raise ValueError('char_code must contain 3 letters')
            else:
                # Spliting char_code by letters
                splited = []
                for i in range(len(value)):
                    splited.append(value[i])
                # Checking char_code for letters repition
                repeated_letters = {}
                for i in range(len(splited)):
                    if splited[i] not in repeated_letters:
                        repeated_letters[splited[i]] = 1
                    else:
                        repeated_letters[splited[i]] += 1
                # Checking char_code for the same letters only
                for i in range(len(repeated_letters)):
                    if repeated_letters[splited[i]] == len(value):
                        raise ValueError('char_code contains only the same letters')
                # Cheking char_code for numbers
                for letter in splited:
                    try:
                        int(letter)
                        raise ValueError('char_code must not contain integer values')
                    except ValueError:
                        pass
                # Checking if char_code containts uppercase letters only
                if value.isupper() == False:
                    raise ValueError('char_code must contain uppercase letters only')
        elif name == 'nominal':
            if type(value) != int:
                raise TypeError('nominal must be of the int type')
        elif name == 'rate':
            if type(value) != float:
                raise TypeError('rate must be of the float type')
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
        object.__setattr__(self, name, value)

    def __eq__(self, other): return self.char_code == other.char_code if type(other) == Currency else False


class CurrencyRepositoryFactory(ModelRepositoryFactory):
    def __init__(self, pgds):
        self.pgds = pgds

    def __str__(self):
        currencies = self.pgds.query('SELECT * FROM currencies')
        if len(currencies) != 0:
            currs = []
            for row in currencies:
                c = self.get_currency(row[0], row[1], row[2], float(row[3]))
                c.inDB = True
                currs.append(c)
            out = ''
            for currency in currs:
                out = out + str(currency)
        else:
            out = '\nNo currencies here\n'
        return out

    def __repr__(self):
        return str(self.pgds.query('SELECT * FROM currencies'))

    # ##### Factory methods #####
    def get_currency(self, num_code, char_code, nominal, rate):
        return Currency(num_code, char_code, nominal, rate)

    # ##### Repository methods #####
    def all(self):
        res = self.pgds.query('SELECT * FROM currencies')
        currencies = []
        if len(res) > 0:
            for row in res:
                c = self.get_currency(row[0], row[1], row[2], float(row[3]))
                c.inDB = True
                currencies.append(c)
        return currencies

    def save(self, currency):
        # Type verify
        if type(currency) != Currency:
            raise TypeError('the entity should be only of the Currency type')
        # Save object data
        if currency.inDB == False:
            currency.num_code = self.pgds.query(f'INSERT INTO currencies\
                VALUES (\'{currency.num_code}\', \'{currency.char_code}\', {currency.nominal}, {currency.rate})\
                RETURNING num_code')[0][0]
            currency.inDB = True
        elif currency.inDB:
            self.pgds.query(f'UPDATE currencies\
                SET num_code = \'{currency.num_code}\', char_code = \'{currency.char_code}\', \
                nominal = {currency.nominal}, rate = {currency.rate}\
                WHERE num_code = \'{currency.num_code}\'')

    def save_many(self, *currencies):
        # Checking object quantity
        l = len(currencies)
        if l in [0, 1]: raise ValueError(f'at least 2 objects can be saved, not {l}')
        # Checking objects type
        for i in range(l):
            if type(currencies[i]) != Currency:
                raise TypeError(f'object number {i+1} is not a Currency type')
        # Save objects data
        [self.save(currency) for currency in currencies]

    def find_by_num_code(self, num_code):
        if type(num_code) != str: raise TypeError('num_code must be str type')
        data = self.pgds.query(f'SELECT * FROM currencies WHERE num_code = \'{num_code}\'')
        if len(data) > 0:
            c = self.get_currency(data[0][0], data[0][1], data[0][2], float(data[0][3]))
            c.inDB = True
            return c
    
    def find_by_char_code(self, char_code):
        if type(char_code) != str: raise TypeError('char_code must be str type')
        data = self.pgds.query(f'SELECT * FROM currencies WHERE char_code = \'{char_code}\'')
        if len(data) > 0:
            c = self.get_currency(data[0][0], data[0][1], data[0][2], float(data[0][3]))
            c.inDB = True
            return c

    def delete_by_num_code(self, num_code):
        if type(num_code) != str: raise TypeError('num_code must be of the str type')
        self.pgds.query(f'DELETE FROM currencies WHERE num_code = \'{num_code}\'')

    def delete_by_char_code(self, char_code):
        if type(char_code) != str: raise TypeError('char_code must be of the str type')
        self.pgds.query(f'DELETE FROM currencies WHERE char_code = \'{char_code}\'')


class CurrencyService:
    def get_currencies(self, count=10):
        from datetime import date
        import requests
        data = requests.get(f'https://www.bnm.md/ru/official_exchange_rates?get_xml=1&date={date.today().strftime("%d.%m.%Y")}').text
        from xml.etree import ElementTree
        root = ElementTree.fromstring(data)
        return [Currency(root[i].find('num_code').text, root[i].find('char_code').text,
            int(root[i].find('Nominal').text), float(root[i].find('Value').text)) for i in range(count)]
