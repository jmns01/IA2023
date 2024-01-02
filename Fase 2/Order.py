from Node import Node
from Client import Client

class Order:
    current_id = 0
    def __init__(self, weight=0, goods=[], origem="", destino="", time="", client=Client()): # nao pode ultrapassar 100 kg
        Order.current_id += 1
        self.id = Order.current_id
        self.weight = weight
        self.goods = goods
        self.start_street = origem
        self.delivery_street = destino
        self.delivery_time = time
        self.client = client

    def __str__(self):
        return "Order " + self.id + " To: " + self.client

    def __repr__(self):
        return "Order " + self.id + " To: " + self.client
    
    def getId(self):
        return self.id

    def getWeight(self):
        return self.weight
    
    def getGoods(self):
        return self.goods
    
    def getStreet(self):
        return self.delivery_street
    
    def getTime(self):
        return self.delivery_time
    
    def getClient(self):
        return self.client
    
    def setId(self, newId):
        self.id = newId

    def setWeight(self, newWeight):
        self.weigth = newWeight
    
    def setGoods(self, newGoods):
        self.goods = newGoods

    def setStreet(self, newStreet):
        self.delivery_street = newStreet

    def setTime(self, newTime):
        self.delivery_time = newTime

    def setClient(self, newClient):
        self.client = newClient

    def __eq__(self, other):
        if other.isinstance(Order):
            return self.id == other.id and self.client == other.client and self.goods == other.goods
        return False
    
    def __hash__(self):
        return hash(self.id)