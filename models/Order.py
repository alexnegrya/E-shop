class Order:
    def __init__(self, _id, itemList, customerId, totalCost, paymentId):
        self.setId(_id)
        self.setItemList(itemList)
        self.setCustomerId(customerId)
        self.setTotalCost(totalCost)
        self.setPaymentId(paymentId)

    def setId(self, _id):
        if self.idValueCheck(_id):
            self._id = _id

    def setItemList(self, itemList):
        if type(itemList) == None:
            raise ValueError("Item List is empty!")
        else:
            self._itemList = itemList

    def setCustomerId(self, customerId):
        if type(customerId) == int:
            if self.idValueCheck(customerId):
                self._customerId = customerId
            else:
                raise ValueError("Customer ID cannot be out of range 1...1 000 000!")
        else:
            raise TypeError("ID Type Error!")

    def setTotalCost(self, totalCost):
        if totalCost < 0:
            raise ValueError("Total Cost cannot be negative!")
        else:
            self._totalCost = totalCost

    def setPaymentId(self, paymentId):
        if self.idValueCheck(paymentId):
            self._paymentId = paymentId
        else:
            raise ValueError("Payment ID cannot be out of range 1...1 000 000!")

    def getItemList(self):
        return self._itemList

    def getId(self):
        return self._id

    def getCustomerId(self):
        return self._customerId

    def getTotalCost(self):
        return self._totalCost

    def getPaymentId(self):
        return self._paymentId

    def __str__(self):
        return f"\n " \
               f"Order ID: {self.getId()}\n " \
               f"Items ordered: {self.getItemList()}\n " \
               f"Customer ID: {self.getCustomerId()}\n " \
               f"Total Cost: {self.getTotalCost()}\n " \
               f"Payment ID: {self.getPaymentId()} \n"

    def __repr__(self):
        return self.__str__()

    def idValueCheck(self, _id):
        if 0 <= int(_id) < 1000000:
            return True
        else:
            from exceptions.WrongIdValue import WrongIdValueException
            raise WrongIdValueException


class OrderRepositoryFactory:
    def __init__(self):
        self._lastCreatedId = 0
        self._orders = []

    def getOrder(self, itemList, customerId, totalCost, paymentId ):
        _id = 0
        obj = Order(_id, itemList, customerId, totalCost, paymentId)
        self._lastCreatedId += 1
        obj._id = self._lastCreatedId
        self.save(obj)
        return obj

    def save(self, order):
        self._orders.append(order)

    def all(self):
        return tuple(self._orders)

    def findById(self, _id):
        for order in self._orders:
            if order._id == _id:
                return order
        return None

    def findByCustomerId(self, customerId):
        customerIdList = []
        for order in self._orders:
            if order._customerId == customerId:
                customerIdList.append(order)
        return customerIdList

    def deleteById(self, _id):
        for order in self._orders:
            if order._id == _id:
                self._orders.remove(order)

