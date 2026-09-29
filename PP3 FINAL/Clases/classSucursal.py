class Sucursal:

    def __init__(self, nombre):
        self.__nombre=nombre
        self.categorias=[]

    def get_nombre(self):
        return self.__nombre

    def agregar_categoria(self, categoria):
        self.categorias.append(categoria)
        
    def get_categorias(self):
        return self.categorias
    
