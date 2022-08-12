from .templates import *


class Contact(Model):
    TABLE = 'contacts'
    FIELDS = ('id', 'type', 'value', 'client_id')
    TEST_VALUES = (1, 'test', 'test', 1)

    def validate_model_field(self, name: str, value):
        if name in ('type', 'value'):
            if type(value) != str: raise TypeError(f'{name} attr must be a string')
            elif value == '' or value.isspace(): raise ValueError(f'{name} attr str must be not empty')
        if name == 'type':
            if len(value) > 50: raise ValueError('type max length is 50 chars')
            self.setattr_value = value[0].upper() + value[1:]
        elif name == 'value' and len(value) > 100: raise ValueError('value max length is 100 chars')
        elif name == 'client_id' and type(value) != int: raise TypeError('client id must have int value')


class ContactsManager(ModelManager):
    MODEL = Contact
