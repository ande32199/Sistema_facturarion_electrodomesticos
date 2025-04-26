class Cliente:
    def __init__(self, id=None, tipo_documento=None, documento=None, nombres=None, 
                 apellidos=None, direccion=None, telefono=None, email=None):
        self.id = id
        self.tipo_documento = tipo_documento  # 'CEDULA', 'RUC', 'PASAPORTE'
        self.documento = documento
        self.nombres = nombres
        self.apellidos = apellidos
        self.direccion = direccion
        self.telefono = telefono
        self.email = email
    
    def to_dict(self):
        """Convierte el objeto Cliente a un diccionario"""
        return {
            'id': self.id,
            'tipo_documento': self.tipo_documento,
            'documento': self.documento,
            'nombres': self.nombres,
            'apellidos': self.apellidos,
            'direccion': self.direccion,
            'telefono': self.telefono,
            'email': self.email
        }
    
    def nombre_completo(self):
        """Devuelve el nombre completo del cliente"""
        return f"{self.nombres} {self.apellidos if self.apellidos else ''}".strip()