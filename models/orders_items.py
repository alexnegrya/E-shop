from .templates import *


class OrderItem(Model):
    TABLE = 'orders_items'
    FIELDS = ('id', 'quantity', 'product_id', 'order_id')
    TEST_VALUES = (1, 1, 1, 1)

    def __validate_model_fields(self, name: str, value):
        if name in ('quantity', 'product_id', 'order_id'):
            if type(value) != int: raise TypeError(f'{" ".join(name.split("_").strip())} must have integer value')


class OrdersItemsManager(ModelManager):
    MODEL = OrderItem
