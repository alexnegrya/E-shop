class Rating:

    

    def __init__(self, id):
        self.id = id
        self.productId = productId
        self.customerId = customerId
        self.stars = stars
        self.review = review



    def __str__(self):
        return f"ID: {self.id}\n Product ID: {self.productId}\n Customer ID: {self.customerId}\n Rating: {self.stars}\n Rewiew: {self.review}\n"

    def __repr__(self):
        return self.__str__()




