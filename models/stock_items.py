from .templates import *


class StockItem(Model):
    TABLE = 'stock_items'
    FIELDS = ('id', 'quantity', 'product_id')
    TEST_VALUES = (1, 1, 1)

    def __validate_model_fields(self, name: str, value):
        if name in ('quantity', 'product_id') and type(value) != int: raise TypeError(f'{name} must have int value')


class StockItemsManager(ModelManager):
    MODEL = StockItem
