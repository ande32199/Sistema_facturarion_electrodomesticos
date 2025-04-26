from django.shortcuts import render
import tkinter as tk
from tkinter import ttk

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Facturación de Electrodomésticos")
        self.geometry("1200x800")
        
        # Crear el notebook (pestañas)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Importar y agregar las vistas
        from views.productos_view import ProductosView
        from views.clientes_view import ClientesView
        from views.facturas_view import FacturasView
        from views.reportes_view import ReportesView
        
        self.productos_view = ProductosView(self.notebook, self)
        self.clientes_view = ClientesView(self.notebook, self)
        self.facturas_view = FacturasView(self.notebook, self)
        self.reportes_view = ReportesView(self.notebook, self)
        
        self.notebook.add(self.productos_view, text="Productos")
        self.notebook.add(self.clientes_view, text="Clientes")
        self.notebook.add(self.facturas_view, text="Facturación")
        self.notebook.add(self.reportes_view, text="Reportes")