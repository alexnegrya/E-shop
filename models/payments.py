from .templates import *


class Payment(Model):
    TABLE = 'payments'
    FIELDS = ('id', 'method', 'price')
    TEST_VALUES = (1, 'test', 1)

    def validate_model_field(self, name: str, value):
        if name == 'method' and type(value) != str: raise TypeError('method must be str type')
        elif name == 'price' and type(value) != int: raise TypeError('price must be int value')


class PaymentsManager(ModelManager):
    MODEL = Payment
