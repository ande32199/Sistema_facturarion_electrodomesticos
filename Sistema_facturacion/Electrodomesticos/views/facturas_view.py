import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime
from Electrodomesticos.factura_controller import FacturaController
from Electrodomesticos.cliente_controller import ClienteController
from Electrodomesticos.producto_controller import ProductoController
from reports.reportes_generator import ReportesGenerator

class FacturasView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.factura_controller = FacturaController()
        self.cliente_controller = ClienteController()
        self.producto_controller = ProductoController()
        self.current_factura = None
        self.create_widgets()
        self.listar_facturas()
        self.cargar_clientes()

    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Frame de búsqueda
        search_frame = ttk.LabelFrame(main_frame, text="Buscar Facturas")
        search_frame.pack(fill=tk.X, pady=5)

        ttk.Label(search_frame, text="Desde:").grid(row=0, column=0, padx=5, pady=5)
        self.fecha_inicio_entry = ttk.Entry(search_frame, width=12)
        self.fecha_inicio_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(search_frame, text="Hasta:").grid(row=0, column=2, padx=5, pady=5)
        self.fecha_fin_entry = ttk.Entry(search_frame, width=12)
        self.fecha_fin_entry.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(search_frame, text="Cliente:").grid(row=0, column=4, padx=5, pady=5)
        self.cliente_combobox = ttk.Combobox(search_frame, width=25)
        self.cliente_combobox.grid(row=0, column=5, padx=5, pady=5, sticky=tk.EW)

        search_btn = ttk.Button(search_frame, text="Buscar", command=self.buscar_facturas)
        search_btn.grid(row=0, column=6, padx=5, pady=5)

        # Treeview para facturas
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree = ttk.Treeview(
            tree_frame,
            columns=('id', 'numero', 'fecha', 'cliente', 'total', 'estado'),
            yscrollcommand=scrollbar.set,
            selectmode='browse'
        )
        self.tree.pack(fill=tk.BOTH, expand=True)

        scrollbar.config(command=self.tree.yview)

        # Configurar columnas
        self.tree.heading('#0', text='ID')
        self.tree.heading('numero', text='Número')
        self.tree.heading('fecha', text='Fecha')
        self.tree.heading('cliente', text='Cliente')
        self.tree.heading('total', text='Total')
        self.tree.heading('estado', text='Estado')

        self.tree.column('#0', width=50, anchor=tk.CENTER)
        self.tree.column('numero', width=120)
        self.tree.column('fecha', width=120)
        self.tree.column('cliente', width=200)
        self.tree.column('total', width=100, anchor=tk.E)
        self.tree.column('estado', width=100, anchor=tk.CENTER)

        # Frame de botones
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=5)

        new_btn = ttk.Button(btn_frame, text="Nueva Factura", command=self.nueva_factura)
        new_btn.pack(side=tk.LEFT, padx=5)

        view_btn = ttk.Button(btn_frame, text="Ver Detalle", command=self.ver_detalle)
        view_btn.pack(side=tk.LEFT, padx=5)

        cancel_btn = ttk.Button(btn_frame, text="Anular Factura", command=self.anular_factura)
        cancel_btn.pack(side=tk.LEFT, padx=5)

        print_btn = ttk.Button(btn_frame, text="Imprimir", command=self.imprimir_factura)
        print_btn.pack(side=tk.LEFT, padx=5)

        report_btn = ttk.Button(btn_frame, text="Generar Reporte", command=self.generar_reporte)
        report_btn.pack(side=tk.LEFT, padx=5)

        refresh_btn = ttk.Button(btn_frame, text="Actualizar", command=self.listar_facturas)
        refresh_btn.pack(side=tk.RIGHT, padx=5)

    def cargar_clientes(self):
        clientes = self.cliente_controller.listar_clientes()
        self.clientes = clientes
        self.cliente_combobox['values'] = [f"{c['nombres']} ({c['documento']})" for c in clientes]

    def listar_facturas(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        facturas = self.factura_controller.listar_facturas()
        for factura in facturas:
            self.tree.insert('', tk.END, 
                text=factura['id'],
                values=(
                    factura['numero_factura'],
                    factura['fecha_emision'].strftime("%Y-%m-%d %H:%M"),
                    factura['cliente_nombre'],
                    f"${factura['total']:.2f}",
                    factura['estado']
                ))

    def buscar_facturas(self):
        fecha_inicio = self.fecha_inicio_entry.get().strip()
        fecha_fin = self.fecha_fin_entry.get().strip()
        cliente_seleccionado = self.cliente_combobox.get()

        cliente_id = None
        if cliente_seleccionado:
            documento = cliente_seleccionado.split('(')[-1].rstrip(')')
            cliente = next((c for c in self.clientes if c['documento'] == documento), None)
            if cliente:
                cliente_id = cliente['id']

        for item in self.tree.get_children():
            self.tree.delete(item)
        
        facturas = self.factura_controller.listar_facturas(fecha_inicio, fecha_fin, cliente_id)
        for factura in facturas:
            self.tree.insert('', tk.END, 
                text=factura['id'],
                values=(
                    factura['numero_factura'],
                    factura['fecha_emision'].strftime("%Y-%m-%d %H:%M"),
                    factura['cliente_nombre'],
                    f"${factura['total']:.2f}",
                    factura['estado']
                ))

    def nueva_factura(self):
        from views.factura_detalle_view import FacturaDetalleView
        self.current_factura = None
        FacturaDetalleView(self, self.guardar_factura)

    def ver_detalle(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione una factura para ver detalle")
            return

        factura_id = self.tree.item(selected[0], 'text')
        factura = self.factura_controller.obtener_factura(factura_id)
        
        if factura:
            from views.factura_detalle_view import FacturaDetalleView
            self.current_factura = factura
            FacturaDetalleView(self, None, factura, readonly=True)

    def anular_factura(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione una factura para anular")
            return

        factura_id = self.tree.item(selected[0], 'text')
        estado = self.tree.item(selected[0], 'values')[4]

        if estado == 'ANULADA':
            messagebox.showinfo("Información", "La factura ya está anulada")
            return

        if messagebox.askyesno("Confirmar", "¿Está seguro de anular esta factura?"):
            try:
                if self.factura_controller.anular_factura(factura_id):
                    messagebox.showinfo("Éxito", "Factura anulada correctamente")
                    self.listar_facturas()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo anular: {str(e)}")

    def imprimir_factura(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione una factura para imprimir")
            return

        factura_id = self.tree.item(selected[0], 'text')
        factura = self.factura_controller.obtener_factura(factura_id)
        
        if factura:
            try:
                filename = filedialog.asksaveasfilename(
                    defaultextension=".pdf",
                    filetypes=[("PDF files", "*.pdf")],
                    title="Guardar factura como"
                )
                if filename:
                    self.factura_controller.generar_pdf_factura(factura_id, filename)
                    messagebox.showinfo("Éxito", f"Factura guardada en {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo generar el PDF: {str(e)}")

    def generar_reporte(self):
        fecha_inicio = self.fecha_inicio_entry.get().strip()
        fecha_fin = self.fecha_fin_entry.get().strip()
        cliente_seleccionado = self.cliente_combobox.get()

        cliente_id = None
        if cliente_seleccionado:
            documento = cliente_seleccionado.split('(')[-1].rstrip(')')
            cliente = next((c for c in self.clientes if c['documento'] == documento), None)
            if cliente:
                cliente_id = cliente['id']

        facturas = self.factura_controller.listar_facturas(fecha_inicio, fecha_fin, cliente_id)
        
        if not facturas:
            messagebox.showinfo("Información", "No hay facturas para generar el reporte")
            return

        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf")],
                title="Guardar reporte como"
            )
            if filename:
                ReportesGenerator.generar_reporte_ventas(facturas, filename)
                messagebox.showinfo("Éxito", f"Reporte generado en {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el reporte: {str(e)}")

    def guardar_factura(self, factura_data):
        try:
            factura_id = self.factura_controller.crear_factura(factura_data)
            messagebox.showinfo("Éxito", f"Factura {factura_data.numero_factura} creada correctamente")
            self.listar_facturas()
            return factura_id
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar la factura: {str(e)}")
            return None