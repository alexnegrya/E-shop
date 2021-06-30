# Address.py module 

class Address:
    def __init__(self, id, country, city, street, number):
        self.id = id
        self.country = country
        self.city = city
        self.street = street
        self.number = number

    def __str__(self):
        return f"Id: {self.id}\nCountry: {self.country}\nCity: {self.city}\nStreet: {self.street}\nNumber: {self.number}"

    def __repr__(self):
        return str(self)