from django.db import models
from datetime import datetime

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

class Factura:
    def __init__(self, id=None, numero_factura=None, cliente_id=None, fecha_emision=None,
                 subtotal=0.0, iva=0.0, descuento=0.0, total=0.0, estado='PENDIENTE',
                 metodo_pago=None, detalles=None):
        self.id = id
        self.numero_factura = numero_factura
        self.cliente_id = cliente_id
        self.fecha_emision = fecha_emision if fecha_emision else datetime.now()
        self.subtotal = subtotal
        self.iva = iva
        self.descuento = descuento
        self.total = total
        self.estado = estado  # 'PENDIENTE', 'PAGADA', 'ANULADA'
        self.metodo_pago = metodo_pago  # 'EFECTIVO', 'TARJETA', 'TRANSFERENCIA', 'CREDITO'
        self.detalles = detalles if detalles else []
    
    def calcular_totales(self, iva_percent=12):
        """Calcula los totales de la factura basado en los detalles"""
        self.subtotal = sum(d['subtotal'] for d in self.detalles)
        self.iva = self.subtotal * (iva_percent / 100)
        self.total = self.subtotal + self.iva - self.descuento
    
    def to_dict(self):
        """Convierte el objeto Factura a un diccionario"""
        return {
            'id': self.id,
            'numero_factura': self.numero_factura,
            'cliente_id': self.cliente_id,
            'fecha_emision': self.fecha_emision,
            'subtotal': self.subtotal,
            'iva': self.iva,
            'descuento': self.descuento,
            'total': self.total,
            'estado': self.estado,
            'metodo_pago': self.metodo_pago,
            'detalles': self.detalles
        }