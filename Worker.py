class worker:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.average_rank = 0 # numero entre 0 e 5
        self.num_deliveries = 0

    def __str__(self):
        return "Estafeta: " + str(self.id) + " -> " + str(self.name)
    
    def getId(self):
        return self.id
    
    def getName(self):
        return self.name
    
    def getRank(self):
        return self.average_rank

    def setId(self, newId):
        self.id = newId

    def setName(self, newName):
        self.name = newName

    def newRank(self, rank):
        self.average_rank = ((self.average_rank*self.num_deliveries) + rank) / self.num_deliveries+1
        self.num_deliveries += 1

    def __eq__(self, other):
        return self.id == other.id and self.name == other.name

    def __hash__(self):
        hash(self.id, self.name)