from .templates import *


class Order(Model):
    TABLE = 'orders'
    FIELDS = ('id', 'total_cost_id', 'payment_id', 'client_id')
    TEST_VALUES = (1, 1, 1, 1)
    WITH_CREATED = True
    WITH_UPDATED = True

    def __validate_model_fields(self, name: str, value):
        if name.endswith('_id') and type(value) != int: raise ValueError(f'{name} must have int value')


class OrdersManager(ModelManager):
    MODEL = Order
