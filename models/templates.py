from services.pg import PostgresORM


class Model:
    def __init__(self, **fields):
        raise NotImplementedError()
    
    def __str__(self):
        raise NotImplementedError()
    
    def __repr__(self):
        raise NotImplementedError()
    
    def __setattr__(self, name, value):
        raise NotImplementedError()
    
    def __eq__(self, other):
        raise NotImplementedError()


class BaseModelRepositoryFactory:
    MODEL = None

    def __init__(self, orm: PostgresORM):
        self.orm = orm
        if self.MODEL == None: raise NotImplementedError('model must be specified')
        self.model_name = self.MODEL.__class__.__name__
    
    def __str__(self):
        raise NotImplementedError()
    
    def __repr__(self):
        raise NotImplementedError()

    def all(self):
        raise NotImplementedError()

    def save(self, obj):
        raise NotImplementedError()

    def save_many(self, *objs):
        raise NotImplementedError()

    def find_by_id(self, id_):
        raise NotImplementedError()
    
    def delete_by_id(self, id_):
        raise NotImplementedError()
