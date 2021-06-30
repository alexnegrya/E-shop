# Address.py module 

class Address:
    def __init__(self, id, country, city, street, number):
        if id<=0 or id>1000000:
            print('Error: not valid id')
        else:
            self.id = id
        self.country = country
        self.city = city
        self.street = street
        self.number = number

    def __str__(self):
        return f"Id: {self.id}\nCountry: {self.country}\nCity: {self.city}\nStreet: {self.street}\nNumber: {self.number}"

    def __repr__(self):
        return str(self)
    
    def __setattr__(self, name, value):
        if name == "id":
            if value<=0 or value>1000000:
                raise Exception("Error. id is not valid")
            else:
                object.__setattr__(self, name, value)
        else:
            object.__setattr__(self, name, value)