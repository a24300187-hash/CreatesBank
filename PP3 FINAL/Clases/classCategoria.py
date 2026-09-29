class Categoria:

    def __init__(self, nombre):
        self.__nombre=nombre
        self.productos=[]

    def get_nombre(self):
        return self.__nombre

    def agregar_producto(self, producto):
        self.productos.append(producto)

    def get_productos(self):
        return self.productos
        