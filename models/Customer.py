class Customer:
    def __init__(self, id, firstName, lastName, addressId):
        self.id = id
        self.firstName = firstName
        self.lastName = lastName
        self.addressId = addressId
    
    def __str__(self):
        return f" - ID customer: {self.id}, \n - First name: {self.firstName}, \n - Last name: {self.lastName}, \n - Adress Id: {self.addressId}"
    
    def __repr__(self):
       return self.__str__()
