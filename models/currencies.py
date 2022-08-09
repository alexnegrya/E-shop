from .templates import *


class Currency(Model):
    TABLE = 'currencies'
    FIELDS = ('num_code', 'char_code', 'nominal', 'rate')
    TEST_VALUES = ('123', 'VAL', 1, 1.1234)

    def __get_attr_for_print(self, attr: str):
        if attr == 'rate': return f'{self.rate:.04f}'

    def __validate_model_fields(self, name: str, value):
        if name == 'num_code':
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
                splited = list(value)
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
            if type(value) != int: raise TypeError('nominal must be of the int type')
        elif name == 'rate':
            if type(value) != float: raise TypeError('rate must be of the float type')
            elif len(f'{value:.04f}'.split('.')[1]) != 4: raise ValueError('rate must be with 4 numbers after the dot')



class CurrenciesManager(ModelManager):
    MODEL = Currency


class CurrencyService:
    def get_currencies(self, count=10):
        from datetime import date
        import requests
        data = requests.get(f'https://www.bnm.md/ru/official_exchange_rates?get_xml=1&date={date.today().strftime("%d.%m.%Y")}').text
        from xml.etree import ElementTree
        root = ElementTree.fromstring(data)
        return [Currency(root[i].find('num_code').text, root[i].find('char_code').text,
            int(root[i].find('Nominal').text), float(root[i].find('Value').text)) for i in range(count)]
