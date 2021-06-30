

class Order:

    def __init__(self, id, itemList, customerId, totalCost, paymentId):
        if idValueCheck(id):
            self.id = id
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


def idValueCheck(id):
    if 1 <= id < 1000000:
        return True
    else:
        from exceptions.WrongIdValue import WrongIdValueException
        raise WrongIdValueException

class OrderRepositoryFactory:
    id_remembered = 0

    def rememberId(self, id_get):
        self.id_remembered = id_get

    def lastCreatedId(self):
        if Order is None:
            lastId = 0
        else:
            # global id_remembered
            lastId = self.id_remembered
        return lastId


    def getOrder(self, itemList, customerId, totalCost, paymentId):
        id_get = self.lastCreatedId() + 1
        self.rememberId(id_get)
        order = Order(id_get, itemList, customerId, totalCost, paymentId)
        return order


