from .templates import *


class Rating(Model):
    TABLE = 'ratings'
    FIELDS = ('id', 'stars', 'review', 'product_id', 'client_id')
    TEST_VALUES = (1, 10, 'Test', 1, 1)
    WITH_CREATED = True
    WITH_UPDATED = True

    def __validate_model_fields(self, name: str, value):
        if name == 'stars':
            if type(value) != int: raise TypeError('stars must be int type')
            if value not in range(1, 11): raise ValueError('stars must be in int range 1-10')
        elif name == 'review':
            if type(value) != str: raise TypeError('review must be str type')
            # Spliting review by letters
            splited = list(value)
            # Checking review for letters repition
            repeated_numbers = {}
            for i in range(len(splited)):
                if splited[i] not in repeated_numbers:
                    repeated_numbers[splited[i]] = 1
                else:
                    repeated_numbers[splited[i]] += 1
            # Checking review for the same letters only
            for i in range(len(repeated_numbers)):
                if repeated_numbers[splited[i]] == len(value):
                    raise AttributeError('the review contains only the same letters')
            # Checking review lenght
            if len(value) > 500:
                raise ValueError('review must contain 500 characters max')
            value = f'"{value}"'
        elif name.endswith('_id') and type(value) != int: raise TypeError(f'{name} must have int value')


class RatingsManager(ModelManager):
    MODEL = Rating
