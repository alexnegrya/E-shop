from .templates import *
import re


class Client(Model):
    TABLE = 'clients'
    FIELDS = ('id', 'email', 'first_name', 'last_name', 'password', 'address_id')
    TEST_VALUES = (1, 'test@test.to', 'test', 'test', 'test1234', 1)
    WITH_CREATED = True
    WITH_UPDATED = True

    def validate_model_field(self, name, value):
        if name == 'email':
            email_pattern = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
            if not re.match(email_pattern, value):
                raise ValueError('wrong email format')
        elif name in ('first_name', 'last_name'):
            if type(value) != str:
                raise TypeError('name must be a string')
            elif value == '':
                raise NameError('name cannot be an empty string')
            else:
                formated_name = name.replace('_', ' ')
                splited = list(value)
                if ' ' in splited: raise ValueError(f'{formated_name} must not contains spaces')
                # Checking name for letters repition
                repeat_numbers = {}
                for i in range(len(splited)):
                    if splited[i] not in repeat_numbers:
                        repeat_numbers[splited[i]] = 1
                    else:
                        repeat_numbers[splited[i]] += 1
                # Checking name for the same letters only
                for i in range(len(repeat_numbers)):
                    if repeat_numbers[splited[i]] == len(value):
                        raise NameError(f'{formated_name} contains only the same letters')
                # Cheking name for numbers
                for letter in splited:
                    try:
                        int(letter)
                        raise NameError(f'{formated_name} must not contain integer values')
                    except ValueError:
                        pass
        elif name == 'password':
            if len(value) < 8:
                raise ValueError('password length must be at least 8 characters')
        elif name == 'address_id':
            if value != None and type(value) != int:
                raise TypeError('wrong type of Address id')


class ClientsManager(ModelManager):
    MODEL = Client
