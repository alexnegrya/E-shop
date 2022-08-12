from services.pg import PostgresDataService
import re
from datetime import datetime
from .tools import get_model_fields


class _StringFormatter:
    def format_to_title(self, string: str, with_capital=True) -> str:
        first_letter = string[0].upper() if with_capital else string[0]
        return first_letter + string[1:].replace('_', ' ')

    def format_with_capital(self, string: str) -> str: return string[0].upper() + string[1:]


class Model:
    """
    Parent class for any DB model. Wrapper for some row in some table, used with manager. `TABLE`, `FIELDS` and `TEST_VALUES` attributes is needed, other is optional.
    Also needed to write code that raises exceptions if any of recieved values for fields (exclude `id`) is wrong in `validate_model_field` method.
    Change `__get_attr_for_print` function to return value of needed attr in the `print` format (optional).
    """

    TABLE = ''
    FIELDS = ()
    TEST_VALUES = ()
    WITH_CREATED = False
    WITH_UPDATED = False

    def __validate_default_attrs(self):
        if self.TABLE == '': raise NotImplementedError()
        elif type(self.TABLE) != str: raise TypeError('TABLE must have str value')
        self.__set_fields()
        if len(self.FIELDS) == 0: raise NotImplementedError()
        elif type(self.FIELDS) != tuple: raise TypeError('FIELDS must be a tuple')
        elif any([type(v) != str for v in self.FIELDS]): raise TypeError('FIELDS must contains only str values')
        if len(self.TEST_VALUES) == 0: raise NotImplementedError()
        elif type(self.TEST_VALUES) != tuple: raise TypeError('TEST_VALUES must be a dict')
        elif len(self.TEST_VALUES) != len(self.FIELDS): raise ValueError('TEST_VALUES values count must be the same as FIELDS count')
        for dt_attr in ('WITH_CREATED', 'WITH_UPDATED'):
            if getattr(self, dt_attr) not in (True, False): raise TypeError(f'{dt_attr} must have only True or False value')

    def __update_doc(self):
        if self.WITH_CREATED and self.WITH_UPDATED: support_info = 'Created and last updated dates saving is supported'
        elif self.WITH_CREATED: support_info = 'Created date saving is supported'
        elif self.WITH_UPDATED: support_info = 'Last updated date saving is supported'
        else: support_info = 'Created and last updated dates saving is NOT supported'
        self.__doc__ = f"DB model to wrap data from {self.TABLE} table with {', '.join(self.FIELDS[:-1])} and {self.FIELDS[-1]} fields. {support_info}."

    def __set_fields(self):
        fields = []
        for field in self.FIELDS:
            sep_count = len(re.findall(r'\|', field))
            if sep_count == 1:
                spl = field.split('|')
                setattr(self, f'__{spl[0]}_alias', spl[1])
                fields.append(spl[0])
            elif sep_count == 0: fields.append(field)
            else: raise ValueError(f'field "{field}" have many alias separators, only one needed')
        self.FIELDS = tuple(fields)

    def __init__(self, **attrs):
        self.__validate_default_attrs()
        self.WITH_ID = 'id' in self.FIELDS
        if self.WITH_CREATED: self.created = datetime.now()
        if self.WITH_UPDATED: self.updated = None
        self.inDB = False

        model_attrs = attrs.copy()
        try: model_attrs.pop(self.FIELDS[0])
        except KeyError: pass
        if tuple(model_attrs.keys()) != self.FIELDS[1:]: raise ValueError('all attrs for model FIELDS (exclude PK) must be specified')
        [setattr(self, attr, value) for attr, value in attrs.items()]
        if self.WITH_ID and 'id' not in attrs: self.id = None

        self.__update_doc()
        self._formatter = _StringFormatter()

    def __get_attr_for_print(self, attr: str): pass

    def __str__(self):
        title = f'--- {self._formatter.format_to_title(self.__class__.__name__)} ---\n'
        id_ = f'ID: {self.id}\n' if self.WITH_ID else ''
        inDB = f'In DB: {self.inDB}\n'
        fields = {field: field if getattr(self, f"__{field}_alias", None) == None else getattr(self, f"__{field}_alias") for field in self.FIELDS[1:]}
        return f'{title}{id_}{inDB}' + '\n'.join([f'{self._formatter.format_to_title(field_name)}:\
 {getattr(self, field) if self.__get_attr_for_print(field) == None else self.__get_attr_for_print(field)}' for field, field_name in fields.items()])
    
    def __repr__(self):
        fields = []
        for field in self.FIELDS:
            attr = self.__get_attr_for_print(field)
            fields.append(attr if attr != None else getattr(self, field))
        values = [self.inDB] + fields
        if self.WITH_ID: values.insert(0, self.id)
        return f'<<{values}>>'

    def __validate_known_field(self, name: str, value):
        if name == 'id':
            if self.inDB:
                if type(value) != int: raise ValueError('id must have an int value')
        elif name == 'inDB':
            if value not in (True, False): raise ValueError('inDB attr must have True/False value only')
        elif name in ('created', 'updated'):
            if not getattr(self, f'WITH_{name.upper()}'): raise ValueError(f'{name} attr is not supported by this model')
            if value != None and type(value) != datetime: raise TypeError(f'{name} must have datetime object value')

    def validate_model_field(self, name: str, value): raise NotImplementedError(f'method not implemeted in "{self.__class__.__name__}" model')
    
    def __setattr__(self, name: str, value):
        self.__validate_known_field(name, value)
        self.validate_model_field(name, value)
        if getattr(self, 'setattr_value', None) == None: object.__setattr__(self, name, value)
        else:
            object.__setattr__(self, name, self.setattr_value)
            object.__setattr__(self, 'setattr_value', None)
        if name != 'updated' and self.WITH_UPDATED: object.__setattr__(self, 'updated', datetime.now())
    
    def __eq__(self, other) -> bool: return getattr(self, self.FIELDS[0]) == getattr(other, self.FIELDS[0]) if type(other) == type(self) else False

    def get_data(self, with_id=False, with_dt_fields=True) -> dict:
        fields = self.FIELDS if with_id else self.FIELDS[1:]
        data = {field: getattr(self, field) for field in fields}
        if with_dt_fields: [data.update({field: getattr(self, field)}) for field in ('created', 'updated') if getattr(self, f'WITH_{field.upper()}')]
        return data

    def get_test_data(self) -> dict: return {field: self.TEST_VALUES[i] for i, field in enumerate(self.FIELDS)}


class ModelManager:
    """
    Parent class for any DB models manager. Have several methods to CRUD models in database, only `MODEL` must be specified.
    """

    MODEL = None

    def __init__(self, pgds: PostgresDataService):
        self.pgds = pgds
        if self.MODEL == None: raise NotImplementedError('model must be specified')
        model_name_spl = re.findall('[A-Z]{1}[a-z]+', self.MODEL.__class__.__name__)
        if len(model_name_spl) > 2: raise ValueError('model name must contains 2 words max')
        self._formatter = _StringFormatter()
        self.plural = self._formatter.format_to_title(self.MODEL.TABLE)
        self.table, self.fields = self.MODEL.TABLE, get_model_fields(self.MODEL)
        self.with_created, self.with_updated = self.MODEL.WITH_CREATED, self.MODEL.WITH_UPDATED
        self.pk = self.fields[0]
        self.__doc__ = f"{self.MODEL.__class__.__name__} models manager with methods for theirs CRUD in DB."
    
    def __str__(self): return ''.join(self.all()) if len(self.all()) > 0 else f'\nNo {self.plural.lower()} here\n'
    
    def __repr__(self): return str(self.pgds.select('*', from_table=self.table))

    def __getattr__(self, name: str):
        if name == 'sort' and self.with_created or self.with_updated: return self.sort

    def __get_wrapped_data(self, data: list[dict]) -> list:
        models = [self.MODEL(**row) for row in data]
        [setattr(m, 'inDB', True) for m in models]
        return models

    def __validate_values(self, values: dict):
        fields = list(self.fields)
        if self.with_created: fields.append('created')
        if self.with_updated: fields.append('updated')
        if any([field not in fields for field in values.keys()]): raise ValueError('unknown field(s) specified')

    def __select_by_pk(self, pk):
        if pk == None: raise TypeError('pk arg do not must be None')
        data = self.pgds.select(*self.fields, from_table=self.table, where=f'{self.pk} = {pk}')
        if len(data) > 1: raise ValueError(f'more then one model with "{pk}" PK found')
        return self.__get_wrapped_data(data)[0]

    def __update_row(self, model: Model):
        data = model.get_data()
        self.__validate_values(data)
        self.pgds.update(self.table, {self.pk: getattr(model, self.pk), }, **data)

    def all(self):
        data = self.pgds.select(*self.fields, from_table=self.table)
        return self.__get_wrapped_data(data)

    def sort(self, *models) -> list:
        l, attrs = [], [attr for attr in ('updated', 'created') if getattr(self, f'with_{attr}')]
        for attr in attrs:
            for dt in sorted([getattr(model, attr) for model in models if getattr(model, attr) != None])[::-1]:
                l += [model for model in models if getattr(model, attr) == dt and model not in l]
        return l + [model for model in models if model not in l]

    def save(self, *models):
        models_pkeys = []
        for model in models:
            if type(model) != self.MODEL: raise TypeError(f'all objects should be only {self.plural} type')
            if model.inDB:
                pk = getattr(model, self.pk)
                self.__update_row(model)
            else: pk = self.pgds.insert(self.table, self.pk, **model.get_data())[0][0]
            models_pkeys.append(pk)
        return [self.find(**{self.pk: pkey}) for pkey in models_pkeys]

    def find(self, **values):
        self.__validate_values(values)
        if tuple(values.keys()) == (self.pk,): return self.__select_by_pk(values[self.pk])
        data = self.pgds.select(*self.fields, from_table=self.table, where={f: v for f, v in values.items()})
        return self.__get_wrapped_data(data)
    
    def delete(self, *models_or_pkeys): [self.pgds.delete(self.table,
        f'{self.pk} = {getattr(obj, self.pk) if type(obj) != int else obj}') for obj in models_or_pkeys]
