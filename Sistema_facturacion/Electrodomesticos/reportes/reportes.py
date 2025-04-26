from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from datetime import datetime

class ReportesGenerator:
    @staticmethod
    def generar_reporte_ventas(facturas, filename="reporte_ventas.pdf"):
        doc = SimpleDocTemplate(filename, pagesize=letter)
        elements = []
        
        # Estilos
        styles = getSampleStyleSheet()
        title_style = styles['Title']
        normal_style = styles['Normal']
        
        # Título
        elements.append(Paragraph("Reporte de Ventas", title_style))
        elements.append(Paragraph(f"Generado el: {datetime.now().strftime('%Y-%m-%d %H:%M')}", normal_style))
        elements.append(Paragraph(" ", normal_style))  # Espacio
        
        # Datos de la tabla
        data = [["N° Factura", "Fecha", "Cliente", "Total", "Estado"]]
        
        for factura in facturas:
            data.append([
                factura['numero_factura'],
                factura['fecha_emision'].strftime('%Y-%m-%d'),
                factura['cliente_nombre'],
                f"${factura['total']:.2f}",
                factura['estado']
            ])
        
        # Crear tabla
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(table)
        doc.build(elements)
        return filename