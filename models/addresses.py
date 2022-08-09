from .templates import *


class Address(Model):
    TABLE = 'addresses'
    FIELDS = ('id', 'country', 'city', 'street', 'number|street number')
    TEST_VALUES = (1, 'test', 'test', 'test', '1/2')

    def __validate_model_fields(self, name: str, value):
        if name in ('country', 'city', 'street'):
            if type(value) != str:
                raise TypeError('value must be a string')
            elif value == '':
                raise ValueError('value cannot be an empty string')
            else:
                # Spliting name by letters
                splited = []
                for i in range(len(value)):
                    splited.append(value[i])
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
                        raise ValueError(
                            'the value contains only the same letters')
        elif name == 'number':
            if type(value) != int and type(value) != str:
                raise TypeError('wrong number type')
            if type(value) == str:
                # Checking str for the content of letters
                if value.isupper() or value.islower():
                    raise ValueError('value must not contain letters')
            self.__value = value.strip()


class AddressesManager(ModelManager):
    MODEL = Address
