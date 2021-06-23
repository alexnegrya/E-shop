class Category:
    def __init__(self, id, name, parentCategoryId=None):
        if type(name) == str and type(id) == str:
            self.name = name
            self.id = id
        else:
            raise TypeError('wrong name or id type')
        if parentCategoryId != None:
            if type(parentCategoryId) == str:
                self.parentCategoryId = parentCategoryId
            else:
                raise TypeError('wrong parentCategoryId type')
        else:
            self.parentCategoryId = None
    
    def __str__(self):
        title = f"--- Category \"{self.name}\" ---"
        id = f"Id: {self.id}"
        if self.parentCategoryId == None:
            parent = 'Have parent category: No'
        else:
            parent = 'Have parent category: Yes'
            parent = parent + '\n' + f'- parent categoty id: {self.parentCategoryId}'
        out = title + '\n' + id + '\n' + parent
        return out
    
    def __repr__(self):
        return str(self)
