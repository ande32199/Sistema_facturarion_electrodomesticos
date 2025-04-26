from datetime import datetime

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