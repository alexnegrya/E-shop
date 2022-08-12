from .templates import *


class Money(Model):
    TABLE = 'money'
    FIELDS = ('id', 'amount')
    TEST_VALUES = (1, 1, 'VAL')

    def validate_model_field(self, name: str, value):
        if name == 'amount' and type(value) not in (int, float):
            raise TypeError('amount must be int or float type')


class MoneyManager(ModelManager):
    MODEL = Money
