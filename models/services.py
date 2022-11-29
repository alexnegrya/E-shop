from .templates import *


class Service(Model):
    TABLE = 'services'
    FIELDS = ('id', 'name', 'description', 'price')
    TEST_VALUES = (1, 'Test', 'Test', 1)

    def validate_model_field(self, name: str, value):
        if name in ('name', 'description'):
            if type(value) != str:
                raise TypeError('value must be a string')
            elif value == '':
                raise NameError('value cannot be an empty string')
            else:
                # Spliting by letters
                splited = list(value)
                # Checking for letters repition
                repeated_numbers = {}
                for i in range(len(splited)):
                    if splited[i] not in repeated_numbers:
                        repeated_numbers[splited[i]] = 1
                    else:
                        repeated_numbers[splited[i]] += 1
                # Checking for the same letters only
                for i in range(len(repeated_numbers)):
                    if repeated_numbers[splited[i]] == len(value):
                        raise NameError('the str value contains only the same letters')
        elif name == 'price' and type(value) != int:
            raise TypeError(f'{name} must have int value')


class ServicesManager(ModelManager): MODEL = Service
