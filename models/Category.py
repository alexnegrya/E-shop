class Category:
    def __init__(self, id, name, parentCategoryId=None):
        if type(name) == str and type(id) == str:
            self.name = name
            self.id = id
            self.parentCategoryId = parentCategoryId
    
    def __str__(self):
        title = f"--- Category \"{self.name}\" ---"
        id = f"Id: {self.id}"
        if self.parentCategoryId == None:
            parent = 'Have parent category: No'
        else:
            parent = 'Have parent category: Yes'
            parent = parent + '\n' + f'- parent categoty id: {self.parentCategoryId}'
        out = '\n' + title + '\n' + id + '\n' + parent + '\n'
        return out
    
    def __repr__(self):
        return str(self)
