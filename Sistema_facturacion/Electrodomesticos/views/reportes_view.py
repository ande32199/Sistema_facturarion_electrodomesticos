import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from Electrodomesticos.factura_controller import FacturaController
from reports.reportes_generator import ReportesGenerator
from datetime import datetime

class ReportesView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.factura_controller = FacturaController()
        self.create_widgets()
    
    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame de filtros
        filter_frame = ttk.LabelFrame(main_frame, text="Filtros de Reporte")
        filter_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(filter_frame, text="Desde:").grid(row=0, column=0, padx=5, pady=5)
        self.fecha_inicio = ttk.Entry(filter_frame)
        self.fecha_inicio.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(filter_frame, text="Hasta:").grid(row=0, column=2, padx=5, pady=5)
        self.fecha_fin = ttk.Entry(filter_frame)
        self.fecha_fin.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(filter_frame, text="Tipo de Reporte:").grid(row=0, column=4, padx=5, pady=5)
        self.tipo_reporte = ttk.Combobox(filter_frame, values=["Ventas", "Productos", "Clientes"])
        self.tipo_reporte.grid(row=0, column=5, padx=5, pady=5)
        self.tipo_reporte.current(0)
        
        # Botones
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        generar_btn = ttk.Button(btn_frame, text="Generar Reporte", command=self.generar_reporte)
        generar_btn.pack(side=tk.LEFT, padx=5)
    
    def generar_reporte(self):
        fecha_inicio = self.fecha_inicio.get().strip()
        fecha_fin = self.fecha_fin.get().strip()
        tipo_reporte = self.tipo_reporte.get()
        
        try:
            if tipo_reporte == "Ventas":
                facturas = self.factura_controller.listar_facturas(fecha_inicio, fecha_fin)
                if not facturas:
                    messagebox.showinfo("Información", "No hay datos para generar el reporte")
                    return
                
                filename = filedialog.asksaveasfilename(
                    defaultextension=".pdf",
                    filetypes=[("PDF files", "*.pdf")],
                    title="Guardar reporte como"
                )
                
                if filename:
                    ReportesGenerator.generar_reporte_ventas(facturas, filename)
                    messagebox.showinfo("Éxito", f"Reporte generado en {filename}")
            
            # Aquí puedes agregar más tipos de reportes
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el reporte: {str(e)}")