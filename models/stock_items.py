from .templates import *


class StockItem(Model):
    TABLE = 'stock_items'
    FIELDS = ('id', 'quantity', 'product_id')
    TEST_VALUES = (1, 1, 1)

    def validate_model_field(self, name: str, value):
        if name == 'quantity':
            if type(value) != int: raise TypeError(f'{name} must be a number')
            elif value < 0: raise ValueError(
                f'{name} cannot have a negative number')
        elif name == 'product_id' and type(value) != int:
            raise TypeError(f'{name} must have int value')


class StockItemsManager(ModelManager):
    MODEL = StockItem
