class Currency:
    def __init__(self, numCode, charCode, nominal, rate):
        self.inDB = False
        self.numCode = numCode
        self.charCode = charCode
        self.nominal = nominal
        self.rate = rate

    def __str__(self):
        title = f"--- Currency ---"
        inDB = f'In DB: {self.inDB}'
        numCode = f"NumCode: {self.numCode}"
        charCode = f'CharCode: {self.charCode}'
        nominal = f'Nominal: {self.nominal}'
        rate = f'Rate: {self.rate:.04f}'
        out = f'\n\n{title}\n{inDB}\n{numCode}\n{charCode}\n{nominal}\n{rate}\n\n'
        return out

    def __repr__(self):
        return f'<<[{self.inDB}, {self.numCode}, {self.charCode}, {self.nominal}, {self.rate:.04f}]>>'

    def __setattr__(self, name, value):
        if name == 'inDB':
            if value in (True, False):
                object.__setattr__(self, name, value)
            else:
                raise TypeError('value for inDB attribute must be True or False only')
        elif name == 'numCode':
            if type(value) != str:
                raise TypeError('value for numCode must be str type')
            elif len(value) != 3:
                raise ValueError('str must contain 3 characters')
            elif value.isnumeric() == False:
                raise ValueError('value must contain only numbers in str')
            else:
                object.__setattr__(self, name, value)
        elif name == 'charCode':
            if type(value) != str:
                raise TypeError('charCode must be a string')
            elif value == '':
                raise ValueError('charCode cannot be an empty string')
            elif len(value) != 3:
                raise ValueError('charCode must contain 3 letters')
            else:
                # Spliting charCode by letters
                splited = []
                for i in range(len(value)):
                    splited.append(value[i])
                # Checking charCode for letters repition
                repeated_letters = {}
                for i in range(len(splited)):
                    if splited[i] not in repeated_letters:
                        repeated_letters[splited[i]] = 1
                    else:
                        repeated_letters[splited[i]] += 1
                # Checking charCode for the same letters only
                for i in range(len(repeated_letters)):
                    if repeated_letters[splited[i]] == len(value):
                        raise ValueError('charCode contains only the same letters')
                # Cheking charCode for numbers
                for letter in splited:
                    try:
                        int(letter)
                        raise ValueError('charCode must not contain integer values')
                    except ValueError:
                        pass
                # Checking if charCode containts uppercase letters only
                if value.isupper() == False:
                    raise ValueError('charCode must contain uppercase letters only')
                object.__setattr__(self, name, value)
        elif name == 'nominal':
            if type(value) != int:
                raise TypeError('nominal must be of the int type')
            else:
                object.__setattr__(self, name, value)
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
                else:
                    object.__setattr__(self, name, value)
        else:
            object.__setattr__(self, name, value)

    def __eq__(self, other):
        if type(other) == Currency:
            if self.id == other.id:
                return True
            else:
                return False


class CurrencyRepositoryFactory:
    def __init__(self, pgds):
        self.pgds = pgds

    def __str__(self):
        currencies = self.pgds.query('SELECT * FROM currencies')
        if len(currencies) != 0:
            currs = []
            for row in currencies:
                c = self.getCurrency(row[0], row[1], row[2], float(row[3]))
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
    def getCurrency(self, numCode, charCode, nominal, rate):
        return Currency(numCode, charCode, nominal, rate)

    # ##### Repository methods #####
    def all(self):
        res = self.pgds.query('SELECT * FROM currencies')
        if len(res) > 0:
            currencies = []
            for row in res:
                c = self.getCurrency(row[0], row[1], row[2], float(row[3]))
                c.inDB = True
                currencies.append(c)
            return currencies
        else:
            return []

    def save(self, currency):
        # Type verify
        if type(currency) != Currency:
            raise TypeError('the entity should be only of the Currency type')
        # Save object data
        if currency.inDB == False:
            currency.numCode = self.pgds.query(f'INSERT INTO currencies\
                VALUES (\'{currency.numCode}\', \'{currency.charCode}\', {currency.nominal}, {currency.rate})\
                RETURNING num_code')[0][0]
            currency.inDB = True
        elif currency.inDB:
            self.pgds.query(f'UPDATE currencies\
                SET num_code = \'{currency.numCode}\', char_code = \'{currency.charCode}\', \
                nominal = {currency.nominal}, rate = {currency.rate}\
                WHERE num_code = \'{currency.numCode}\'')

    def save_many(self, *currencies):
        # Checking object quantity
        l = len(currencies)
        if l in [0, 1]:
            raise ValueError(f'at least 2 objects can be saved, not {l}')
        # Checking objects type
        for i in range(len(currencies)):
            if type(currencies[i]) != Currency:
                raise TypeError(f'object number {i+1} is not a Currency type')
        # Save objects data
        for currency in currencies:
            if currency.inDB == False:
                self.pgds.query(f'INSERT INTO currencies\
                    VALUES (\'{currency.numCode}\', \'{currency.charCode}\', {currency.nominal}, {currency.rate})')
                query = self.pgds.query(
                    f'SELECT num_code FROM currencies WHERE num_code = \'{currency.numCode}\'')
                if len(query) == 1:
                    currency.inDB = True
            elif currency.inDB:
                self.pgds.query(f'UPDATE currencies\
                    SET num_code = \'{currency.numCode}\', char_code = \'{currency.charCode}\', \
                    nominal = {currency.nominal}, rate = {currency.rate}\
                    WHERE num_code = \'{currency.numCode}\'')

    def findByNumCode(self, numCode):
        # Checking type
        if type(numCode) != str:
            raise TypeError('numCode must be str type')
        # Search and return
        data = self.pgds.query(f'SELECT * FROM currencies WHERE num_code = \'{numCode}\'')
        if len(data) > 0:
            c = self.getCurrency(data[0][0], data[0][1], data[0][2], float(data[0][3]))
            c.inDB = True
            return c
    
    def findByCharCode(self, charCode):
        # Checking type
        if type(charCode) != str:
            raise TypeError('charCode must be str type')
        # Search and return
        data = self.pgds.query(f'SELECT * FROM currencies WHERE char_code = \'{charCode}\'')
        if len(data) > 0:
            c = self.getCurrency(data[0][0], data[0][1], data[0][2], float(data[0][3]))
            c.inDB = True
            return c

    def deleteByNumCode(self, numCode):
        # Checking type
        if type(numCode) != str:
            raise TypeError('numCode must be of the str type')
        # Delete data
        self.pgds.query(f'DELETE FROM currencies WHERE num_code = \'{numCode}\'')

    def deleteByCharCode(self, charCode):
        # Checking type
        if type(charCode) != str:
            raise TypeError('charCode must be of the str type')
        # Delete data
        self.pgds.query(f'DELETE FROM currencies WHERE char_code = \'{charCode}\'')


class CurrencyService:
    def getCurrencies(self, count=10):
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
        for i in range(count):
            c = Currency(root[i].find('NumCode').text, root[i].find('CharCode').text,
             int(root[i].find('Nominal').text), float(root[i].find('Value').text))
            out.append(c)
        return out
