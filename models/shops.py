from .templates import *
from datetime import time


class Shop(Model):
    TABLE = 'shops'
    FIELDS = ('id', 'working_hours', 'address_id')
    TEST_VALUES = (1, [['00:00', '00:01'] for _ in range(7)], 1)
    
    def validate_model_field(self, name: str, value):
        if name == 'working_hours':
            # Checking attribute type
            if type(value) != list: raise TypeError(
                'working_hours must be list type')
            # Check working_hours list lenght
            if len(value) != 7: raise TypeError('the working_hours list should contain' + 
                    'seven lists for 7 days of the week')
            # Checking lists in the working_hours list
            working_hours = []
            for i in range(len(value)):
                # Checking  type
                if type(value[i]) != list:
                    raise TypeError(f'object with index {i} in working_hours not is list')
                # Checking length
                if len(value[i]) != 2:
                    raise ValueError(f'list with index {i} contain' +
                    f' {len(value[i])} objects, not 2' +
                    ' (start work time, end work time)')
                # Checking values in the working_hours lists
                day_wh = []
                for v in range(len(value[i])):
                    # Checking type
                    if type(value[i][v]) != time: raise TypeError('list with' +
                        f'index {i} in working_hours contain not str type' +
                        f'object with index {v}')
                    day_wh.append(value[i][v].strftime('%H:%M'))
                working_hours.append(day_wh)
            self.setattr_value = working_hours
        elif name == 'address_id' and type(value) != int: raise TypeError('address_id must be int type')


class ShopsManager(ModelManager):
    MODEL = Shop
