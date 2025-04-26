from database.db_connection import DatabaseConnection
from models.factura import Factura
from datetime import datetime

class FacturaController:
    def __init__(self):
        self.db = DatabaseConnection()
    
    def generar_numero_factura(self):
        """Genera un número de factura único con formato FAC-YYYYMMDD-0001"""
        prefix = "FAC-"
        today = datetime.now().strftime("%Y%m%d")
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "SELECT COUNT(*) FROM facturas WHERE numero_factura LIKE %s",
                (f"{prefix}{today}%",)
            )
            count = cursor.fetchone()[0] + 1
            return f"{prefix}{today}-{count:04d}"
        finally:
            cursor.close()
    
    def crear_factura(self, factura):
        """Crea una nueva factura en la base de datos"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        try:
            # Insertar factura
            cursor.execute(
                "INSERT INTO facturas (numero_factura, cliente_id, fecha_emision, "
                "subtotal, iva, descuento, total, estado, metodo_pago) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (factura.numero_factura, factura.cliente_id, factura.fecha_emision,
                 factura.subtotal, factura.iva, factura.descuento, factura.total,
                 factura.estado, factura.metodo_pago)
            )
            factura_id = cursor.lastrowid
            
            # Insertar detalles
            for detalle in factura.detalles:
                cursor.execute(
                    "INSERT INTO detalles_factura (factura_id, producto_id, cantidad, "
                    "precio_unitario, subtotal) VALUES (%s, %s, %s, %s, %s)",
                    (factura_id, detalle['producto_id'], detalle['cantidad'],
                     detalle['precio_unitario'], detalle['subtotal'])
                )
                
                # Actualizar stock
                cursor.execute(
                    "UPDATE productos SET stock = stock - %s WHERE id = %s",
                    (detalle['cantidad'], detalle['producto_id'])
                )
            
            # Registrar en historial
            cursor.execute(
                "INSERT INTO historial_ventas (factura_id, usuario, accion) "
                "VALUES (%s, %s, %s)",
                (factura_id, 'SISTEMA', 'CREACION')
            )
            
            conn.commit()
            return factura_id
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
    
    def obtener_factura(self, factura_id):
        """Obtiene una factura completa con sus detalles"""
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            # Obtener factura
            cursor.execute(
                "SELECT f.*, c.nombres as cliente_nombre, c.documento as cliente_documento "
                "FROM facturas f JOIN clientes c ON f.cliente_id = c.id "
                "WHERE f.id = %s", (factura_id,)
            )
            factura = cursor.fetchone()
            if not factura:
                return None
            
            # Obtener detalles
            cursor.execute(
                "SELECT df.*, p.nombre as producto_nombre, p.codigo as producto_codigo "
                "FROM detalles_factura df "
                "JOIN productos p ON df.producto_id = p.id "
                "WHERE df.factura_id = %s", (factura_id,)
            )
            detalles = cursor.fetchall()
            
            factura['detalles'] = detalles
            return factura
        finally:
            cursor.close()
    
    def listar_facturas(self, fecha_inicio=None, fecha_fin=None, cliente_id=None):
        """Lista facturas con filtros opcionales"""
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            query = """
                SELECT f.*, c.nombres as cliente_nombre, c.documento as cliente_documento 
                FROM facturas f 
                JOIN clientes c ON f.cliente_id = c.id
            """
            params = []
            conditions = []
            
            if fecha_inicio and fecha_fin:
                conditions.append("f.fecha_emision BETWEEN %s AND %s")
                params.extend([fecha_inicio, fecha_fin])
            elif fecha_inicio:
                conditions.append("f.fecha_emision >= %s")
                params.append(fecha_inicio)
            elif fecha_fin:
                conditions.append("f.fecha_emision <= %s")
                params.append(fecha_fin)
            
            if cliente_id:
                conditions.append("f.cliente_id = %s")
                params.append(cliente_id)
            
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
            
            query += " ORDER BY f.fecha_emision DESC"
            
            cursor.execute(query, tuple(params))
            return cursor.fetchall()
        finally:
            cursor.close()
    
    def anular_factura(self, factura_id):
        """Anula una factura y revierte el stock"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        try:
            # Verificar si ya está anulada
            cursor.execute("SELECT estado FROM facturas WHERE id = %s", (factura_id,))
            estado = cursor.fetchone()[0]
            if estado == 'ANULADA':
                return False
            
            # Obtener detalles para revertir stock
            cursor.execute(
                "SELECT producto_id, cantidad FROM detalles_factura WHERE factura_id = %s",
                (factura_id,)
            )
            detalles = cursor.fetchall()
            
            # Revertir stock
            for producto_id, cantidad in detalles:
                cursor.execute(
                    "UPDATE productos SET stock = stock + %s WHERE id = %s",
                    (cantidad, producto_id)
                )
            
            # Anular factura
            cursor.execute(
                "UPDATE facturas SET estado = 'ANULADA' WHERE id = %s",
                (factura_id,)
            )
            
            # Registrar en historial
            cursor.execute(
                "INSERT INTO historial_ventas (factura_id, usuario, accion) "
                "VALUES (%s, %s, %s)",
                (factura_id, 'SISTEMA', 'ANULACION')
            )
            
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
    
    def obtener_ventas_por_producto(self, producto_id, fecha_inicio=None, fecha_fin=None):
        """Obtiene el historial de ventas de un producto específico"""
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            query = """
                SELECT df.cantidad, df.precio_unitario, df.subtotal, 
                       f.numero_factura, f.fecha_emision, c.nombres as cliente_nombre
                FROM detalles_factura df
                JOIN facturas f ON df.factura_id = f.id
                JOIN clientes c ON f.cliente_id = c.id
                WHERE df.producto_id = %s AND f.estado != 'ANULADA'
            """
            params = [producto_id]
            
            if fecha_inicio and fecha_fin:
                query += " AND f.fecha_emision BETWEEN %s AND %s"
                params.extend([fecha_inicio, fecha_fin])
            elif fecha_inicio:
                query += " AND f.fecha_emision >= %s"
                params.append(fecha_inicio)
            elif fecha_fin:
                query += " AND f.fecha_emision <= %s"
                params.append(fecha_fin)
            
            query += " ORDER BY f.fecha_emision DESC"
            
            cursor.execute(query, tuple(params))
            return cursor.fetchall()
        finally:
            cursor.close()
# Añadir al FacturaController
def generar_pdf_factura(self, factura_id, filename):
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib import colors
    
    factura = self.obtener_factura(factura_id)
    if not factura:
        raise ValueError("Factura no encontrada")
    
    doc = SimpleDocTemplate(filename, pagesize=letter)
    elements = []
    
    styles = getSampleStyleSheet()
    
    # Encabezado
    elements.append(Paragraph("FACTURA", styles['Title']))
    elements.append(Paragraph(f"Número: {factura['numero_factura']}", styles['Normal']))
    elements.append(Paragraph(f"Fecha: {factura['fecha_emision'].strftime('%Y-%m-%d %H:%M')}", styles['Normal']))
    elements.append(Paragraph(f"Cliente: {factura['cliente_nombre']}", styles['Normal']))
    elements.append(Paragraph(" ", styles['Normal']))
    
    # Detalles de la factura
    data = [["Código", "Producto", "Cantidad", "P. Unitario", "Subtotal"]]
    
    for detalle in factura['detalles']:
        data.append([
            detalle['producto_codigo'],
            detalle['producto_nombre'],
            str(detalle['cantidad']),
            f"${detalle['precio_unitario']:.2f}",
            f"${detalle['subtotal']:.2f}"
        ])
    
    # Totales
    data.append(["", "", "", "Subtotal:", f"${factura['subtotal']:.2f}"])
    data.append(["", "", "", "IVA:", f"${factura['iva']:.2f}"])
    if factura['descuento'] > 0:
        data.append(["", "", "", "Descuento:", f"${factura['descuento']:.2f}"])
    data.append(["", "", "", "TOTAL:", f"${factura['total']:.2f}"])
    
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('SPAN', (0, -4), (2, -4)),
        ('SPAN', (0, -3), (2, -3)),
        ('SPAN', (0, -2), (2, -2)),
        ('SPAN', (0, -1), (2, -1)),
        ('FONTNAME', (-2, -4), (-1, -1), 'Helvetica-Bold'),
    ]))
    
    elements.append(table)
    doc.build(elements)
    return filename