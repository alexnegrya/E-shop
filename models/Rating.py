class Rating:

    

    def __init__(self, id, productId, customerId, stars, review):
        self.id = id
        self.productId = productId
        self.customerId = customerId
        self.stars = stars
        self.review = review



    def __str__(self):
        return f"ID: {self.id}\n Product ID: {self.productId}\n Customer ID: {self.customerId}\n Rating: {self.stars}\n Rewiew: {self.review}\n"

    def __repr__(self):
        return self.__str__()



#     def __setattr__(self):
#         return self.id


#     def __getattr__(self, value):
#         if value != int(value):
#             raise TypeError("idValue must be an integer")
#         if 1 <= value <= 1000000:
#             self._idValue = int(value)
#         else:
#             raise ValueError("id must be between 1 and 1000000 inclusive")
