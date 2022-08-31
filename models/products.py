from .templates import *


class Product(Model):
    TABLE = 'products'
    FIELDS = ('id', 'name', 'price', 'category_id')
    TEST_VALUES = (1, 'Test', 1, 1)
    WITH_CREATED = True
    WITH_UPDATED = True

    def validate_model_field(self, name: str, value):
        if name == 'name':
            if type(value) != str:
                raise TypeError('name must be a string')
            elif value == '':
                raise NameError('name cannot be an empty string')
            else:
                # Spliting name by letters
                splited = list(value)
                # Checking name for letters repition
                repeated_numbers = {}
                for i in range(len(splited)):
                    if splited[i] not in repeated_numbers:
                        repeated_numbers[splited[i]] = 1
                    else:
                        repeated_numbers[splited[i]] += 1
                # Checking name for the same letters only
                for i in range(len(repeated_numbers)):
                    if repeated_numbers[splited[i]] == len(value):
                        raise NameError(
                            'the name contains only the same letters')
        elif type(value) != int: raise TypeError(f'{name} must have int value')


class ProductsManager(ModelManager):
    MODEL = Product