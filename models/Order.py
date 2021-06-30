import uuid

class Order:
    def __init__(self, itemList, customerId, totalCost, paymentId):
        self.id = uuid.uuid4()
        self.itemList = itemList
        self.customerId = customerId
        self.totalCost = totalCost
        self.paymentId = paymentId

    def __str__(self):
        return f"\n " \
               f"Order ID: {self.id}\n " \
               f"Items ordered: {self.itemList}\n " \
               f"Customer ID: {self.customerId}\n " \
               f"Total Cost: {self.totalCost}\n " \
               f"Payment ID: {self.paymentId} \n"

    def __repr__(self):
        return self.__str__()
