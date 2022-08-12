from .templates import *


class Money(Model):
    TABLE = 'money'
    FIELDS = ('id', 'amount', 'currency_char_code')
    TEST_VALUES = (1, 1, 'VAL')

    def validate_model_field(self, name: str, value):
        if name == 'amount':
            if type(value) not in (int, float): raise TypeError('amount must be int or float type')
        elif name == 'currency_char_code':
            if type(value) != str: raise TypeError('wrong currency_char_code type, it must be only str')


class MoneyManager(ModelManager):
    MODEL = Money
