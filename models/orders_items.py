from .templates import *


class OrderItem(Model):
    TABLE = 'orders_items'
    FIELDS = ('id', 'quantity', 'product_id', 'order_id')
    TEST_VALUES = (1, 1, 1, 1)

    def validate_model_field(self, name: str, value):
        if name == 'quantity':
            if type(value) != int: raise TypeError(f'{name} must be a number')
            elif value < 1: raise ValueError(f'{name} must be greater than 0')
        elif name in ('product_id', 'order_id'):
            if type(value) != int: raise TypeError(
                f'{" ".join(name.split("_").strip())} must have integer value')


class OrdersItemsManager(ModelManager): MODEL = OrderItem
