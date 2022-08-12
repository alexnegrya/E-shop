from .templates import *
from datetime import datetime


class Category(Model):
    TABLE = 'categories'
    FIELDS = ('id', 'name', 'parent_category_id')
    TEST_VALUES = (1, 'Test', None)
    WITH_CREATED = True
    WITH_UPDATED = True

    def validate_model_field(self, name: str, value):
        if name == 'name':
            if type(value) != str: raise TypeError('name must be a string')
            elif value == '': raise NameError('name cannot be an empty string')
            else:
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
                        raise NameError('the name contains only the same letters')
                # Cheking name for numbers
                for letter in splited:
                    try:
                        int(letter)
                        raise NameError('the name must not contain integer values')
                    except ValueError:
                        pass
                object.__setattr__(self, name, value)
        elif name == 'parent_category_id':
            if type(value) != int and value != None: raise TypeError('wrong parent Category id')
        elif name in ('created', 'updated'):
            if value != None and type(value) != datetime: raise TypeError('created or updated must have datetime object value')


class CategoriesManager(ModelManager):
    MODEL = Category
