from .templates import *


class Shop(Model):
    TABLE = 'shops'
    FIELDS = ('id', 'working_hours', 'address_id')
    TEST_VALUES = (1, [['00:00', '00:01'] for _ in range(7)], 1)
    
    def __validate_model_fields(self, name: str, value):
        if name == 'working_hours':
            # Checking attribute type
            if type(value) != list: raise TypeError('working_hours must be list type')
            # Check working_hours list lenght
            if len(value) != 7:
                raise TypeError(
                    'the working_hours list should contain seven lists for 7 days of the week')
            # Checking lists in the working_hours list
            for i in range(len(value)):
                # Checking  type
                if type(value[i]) != list:
                    raise TypeError(f'object with index {i} in working_hours not is list')
                # Checking length
                if len(value[i]) != 2:
                    raise ValueError(
                        f'list with index {i} contain {len(value[i])} objects, not 2 (start work time, end work time)')
                # Checking values in the working_hours lists
                start_work, end_work = '', ''
                for v in range(len(value[i])):
                    # Checking type
                    if type(value[i][v]) != str:
                        raise TypeError(f'list with index {i} in working_hours contain not str type object with index {v}')
                    wrong_value = f'value with index {v} in list with index {i}'

                    # Checking str lenght
                    if len(value[i][v]) != 5: raise ValueError(f'{wrong_value} not contain 5 characters')

                    # Checking format
                    spl = value[i][v].split(':')
                    if len(spl) != 2: raise ValueError(f'{wrong_value} must be in correct format (00:00)')
                    if spl[0].isnumeric() == False: raise ValueError(f'{wrong_value} contain not numeric hours value')
                    if spl[1].isnumeric() == False: raise ValueError(f'{wrong_value} contain not numeric minutes value')
                    spl = [int(spl[0]), int(spl[1])]
                    if len(spl[0]) < 0: raise ValueError(f'{wrong_value} has negative hours value')
                    if len(spl[0]) > 23: raise ValueError(f'{wrong_value} has hours value more then 23')
                    if len(spl[1]) < 0: raise ValueError(f'{wrong_value} has negative minutes value')
                    if len(spl[1]) > 59: raise ValueError(f'{wrong_value} has minutes value more then 59')

                    # Start work and end work time definition
                    if v == 0: start_work = value[i][v]
                    elif v == 1: end_work = value[i][v]
                
                # Checking if end work > start work time value
                times_spls = [[int(v) for v in var.split(':')] for var in (start_work, end_work)]
                if times_spls[0][0] >= times_spls[1][0] and times_spls[0][1] >= times_spls[1][1]:
                    raise ValueError('start work time must be lesser then end work time')
                
                # Appending start work and end work time definition
                times_defs = [[str(times_spls[0][time_num] - times_spls[1][time_num]) if \
                    times_spls[0][time_num] - times_spls[1][time_num] > 9 else \
                    f'0{times_spls[0][time_num] - times_spls[1][time_num]}'] for time_num in range(2)]
                value[i].append(f'{times_defs[0]}:{times_defs[1]}')
            self.__value = value
        elif name == 'address_id' and type(value) != int: raise TypeError('address_id must be int type')


class ShopsManager(ModelManager):
    MODEL = Shop
