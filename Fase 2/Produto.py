
class Produto:
    def __int__(self, nome="", peso=0.0, preco=0.0):
        self.name = nome
        self.peso = peso

    def getName(self):
        return self.name

    def getPeso(self):
        return self.peso

    def getPreco(self):
        return self.preco