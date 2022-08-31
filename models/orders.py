from .templates import *


class Order(Model):
    TABLE = 'orders'
    FIELDS = ('id', 'total_cost', 'payment_id', 'client_id')
    TEST_VALUES = (1, 1, 1, 1)
    WITH_CREATED = True
    WITH_UPDATED = True

    def validate_model_field(self, name: str, value):
        if type(value) != int: raise ValueError(f'{name} must have int value')


class OrdersManager(ModelManager):
    MODEL = Order
