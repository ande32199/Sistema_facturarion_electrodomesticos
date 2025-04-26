import tkinter as tk
from tkinter import ttk
from views.productos_view import ProductosView
from views.clientes_view import ClientesView
from views.facturas_view import FacturasView
from views.reportes_view import ReportesView

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Configuración de la ventana principal
        self.title("Sistema de Facturación de Electrodomésticos")
        self.geometry("1200x800")
        self.state('zoomed')  # Maximizar la ventana
        
        # Configurar el icono (opcional)
        try:
            self.iconbitmap('icon.ico')  # Asegúrate de tener un archivo icon.ico
        except:
            pass  # Si no hay icono, continuar sin él
        
        # Crear el contenedor principal
        self.create_widgets()
        
        # Configurar el menú superior
        self.configure_menu()

    def create_widgets(self):
        # Crear el notebook (pestañas)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Crear las vistas
        self.productos_view = ProductosView(self.notebook, self)
        self.clientes_view = ClientesView(self.notebook, self)
        self.facturas_view = FacturasView(self.notebook, self)
        self.reportes_view = ReportesView(self.notebook, self)
        
        # Añadir las vistas al notebook
        self.notebook.add(self.productos_view, text="📦 Productos")
        self.notebook.add(self.clientes_view, text="👥 Clientes")
        self.notebook.add(self.facturas_view, text="🧾 Facturación")
        self.notebook.add(self.reportes_view, text="📊 Reportes")

    def configure_menu(self):
        # Crear la barra de menú
        menubar = tk.Menu(self)
        
        # Menú Archivo
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Salir", command=self.quit)
        menubar.add_cascade(label="Archivo", menu=file_menu)
        
        # Menú Ayuda
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Acerca de...", command=self.show_about)
        menubar.add_cascade(label="Ayuda", menu=help_menu)
        
        self.config(menu=menubar)

    def show_about(self):
        about_window = tk.Toplevel(self)
        about_window.title("Acerca del Sistema")
        about_window.geometry("400x300")
        about_window.resizable(False, False)
        
        tk.Label(
            about_window, 
            text="Sistema de Facturación de Electrodomésticos\n\n"
                 "Versión 1.0\n\n"
                 "Desarrollado por:\n[Tu Nombre o Empresa]\n\n"
                 "© 2023 Todos los derechos reservados",
            font=('Arial', 12),
            justify=tk.CENTER,
            pady=20
        ).pack(expand=True)
        
        tk.Button(
            about_window, 
            text="Cerrar", 
            command=about_window.destroy
        ).pack(pady=10)

    def change_view(self, view_name):
        """Cambia a la vista especificada"""
        views = {
            'productos': 0,
            'clientes': 1,
            'facturas': 2,
            'reportes': 3
        }
        self.notebook.select(views[view_name.lower()])