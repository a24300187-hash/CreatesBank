class Producto:
    def __init__(self, nombre, precio, existencia):
        self.__nombre=nombre
        self.__precio=precio
        self.__existencia=existencia
    #getters
    def get_nombre(self):
        return self.__nombre
    def get_precio(self):
        return self.__precio
    def get_existencia(self):
        return self.__existencia
    
    #setters
    def set_nombre(self, nombre):
        self.__nombre=nombre
    def set_precio(self, precio):
        self.__precio=precio
    def set_existencia(self, existencia):
        self.__existencia=existencia
    def get_stock(self):
        return self.__existencia

    def __str__(self):
        return f"Nombre: {self.__nombre} - Precio: ${self.__precio} - Existencias: ({self.__existencia} en stock)"