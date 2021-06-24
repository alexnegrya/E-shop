class Product:
    def __init__(self,id, name, categoryId, price):
        self.id = id
        self.name = name
        self.categoryId = categoryId
        self.price = price
       
    def __str__(self):
        return f"\n " \
               f"Order ID: {self.id}\n " \
               f"Items ordered: {self.name}\n " \
               f"Customer ID: {self.categoryId}\n " \
               f"Total Cost: {self.price}\n " \
               
    def __repr__(self):
        return str(self)