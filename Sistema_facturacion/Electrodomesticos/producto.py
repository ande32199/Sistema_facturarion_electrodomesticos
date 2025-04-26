class Producto:
    def __init__(self, id=None, codigo=None, nombre=None, marca=None, modelo=None, 
                 precio=0.0, stock=0, categoria_id=None, descripcion=None):
        self.id = id
        self.codigo = codigo
        self.nombre = nombre
        self.marca = marca
        self.modelo = modelo
        self.precio = precio
        self.stock = stock
        self.categoria_id = categoria_id
        self.descripcion = descripcion
    
    def to_dict(self):
        """Convierte el objeto Producto a un diccionario"""
        return {
            'id': self.id,
            'codigo': self.codigo,
            'nombre': self.nombre,
            'marca': self.marca,
            'modelo': self.modelo,
            'precio': self.precio,
            'stock': self.stock,
            'categoria_id': self.categoria_id,
            'descripcion': self.descripcion
        }