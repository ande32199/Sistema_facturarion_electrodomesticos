import tkinter as tk
from tkinter import ttk, messagebox
from Electrodomesticos.producto_controller import ProductoController
from Electrodomesticos.categoria_controller import CategoriaController

class ProductosView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.producto_controller = ProductoController()
        self.categoria_controller = CategoriaController()
        self.create_widgets()
        self.listar_productos()
        self.cargar_categorias()

    def create_widgets(self):
        # Frame principal con scrollbar
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Frame de búsqueda
        search_frame = ttk.LabelFrame(main_frame, text="Buscar Producto")
        search_frame.pack(fill=tk.X, pady=5)

        ttk.Label(search_frame, text="Buscar:").grid(row=0, column=0, padx=5, pady=5)
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)

        search_btn = ttk.Button(search_frame, text="Buscar", command=self.buscar_producto)
        search_btn.grid(row=0, column=2, padx=5, pady=5)

        # Treeview para listar productos
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree = ttk.Treeview(
            tree_frame,
            columns=('id', 'codigo', 'nombre', 'marca', 'modelo', 'precio', 'stock', 'categoria'),
            yscrollcommand=scrollbar.set,
            selectmode='browse'
        )
        self.tree.pack(fill=tk.BOTH, expand=True)

        scrollbar.config(command=self.tree.yview)

        # Configurar columnas
        self.tree.heading('#0', text='ID')
        self.tree.heading('codigo', text='Código')
        self.tree.heading('nombre', text='Nombre')
        self.tree.heading('marca', text='Marca')
        self.tree.heading('modelo', text='Modelo')
        self.tree.heading('precio', text='Precio')
        self.tree.heading('stock', text='Stock')
        self.tree.heading('categoria', text='Categoría')

        self.tree.column('#0', width=50, anchor=tk.CENTER)
        self.tree.column('codigo', width=100)
        self.tree.column('nombre', width=150)
        self.tree.column('marca', width=100)
        self.tree.column('modelo', width=100)
        self.tree.column('precio', width=80, anchor=tk.E)
        self.tree.column('stock', width=60, anchor=tk.CENTER)
        self.tree.column('categoria', width=120)

        # Frame de botones
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=5)

        add_btn = ttk.Button(btn_frame, text="Agregar", command=self.abrir_formulario)
        add_btn.pack(side=tk.LEFT, padx=5)

        edit_btn = ttk.Button(btn_frame, text="Editar", command=self.editar_producto)
        edit_btn.pack(side=tk.LEFT, padx=5)

        delete_btn = ttk.Button(btn_frame, text="Eliminar", command=self.eliminar_producto)
        delete_btn.pack(side=tk.LEFT, padx=5)

        refresh_btn = ttk.Button(btn_frame, text="Actualizar", command=self.listar_productos)
        refresh_btn.pack(side=tk.RIGHT, padx=5)

    def cargar_categorias(self):
        self.categorias = self.categoria_controller.listar_categorias()
        self.categoria_dict = {cat['id']: cat['nombre'] for cat in self.categorias}

    def listar_productos(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        productos = self.producto_controller.listar_productos()
        for producto in productos:
            categoria_nombre = self.categoria_dict.get(producto['categoria_id'], '')
            self.tree.insert('', tk.END, 
                text=producto['id'],
                values=(
                    producto['codigo'],
                    producto['nombre'],
                    producto['marca'],
                    producto['modelo'],
                    f"${producto['precio']:.2f}",
                    producto['stock'],
                    categoria_nombre
                ))

    def buscar_producto(self):
        criterio = self.search_entry.get().strip()
        if not criterio:
            self.listar_productos()
            return
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        productos = self.producto_controller.buscar_productos(criterio)
        for producto in productos:
            categoria_nombre = self.categoria_dict.get(producto['categoria_id'], '')
            self.tree.insert('', tk.END, 
                text=producto['id'],
                values=(
                    producto['codigo'],
                    producto['nombre'],
                    producto['marca'],
                    producto['modelo'],
                    f"${producto['precio']:.2f}",
                    producto['stock'],
                    categoria_nombre
                ))

    def abrir_formulario(self, producto=None):
        form = tk.Toplevel(self)
        form.title("Agregar Producto" if not producto else "Editar Producto")
        form.transient(self)
        form.grab_set()

        # Variables de control
        codigo_var = tk.StringVar(value=producto['codigo'] if producto else '')
        nombre_var = tk.StringVar(value=producto['nombre'] if producto else '')
        marca_var = tk.StringVar(value=producto['marca'] if producto else '')
        modelo_var = tk.StringVar(value=producto['modelo'] if producto else '')
        precio_var = tk.StringVar(value=str(producto['precio']) if producto else '0.00')
        stock_var = tk.StringVar(value=str(producto['stock']) if producto else '0')
        categoria_var = tk.StringVar()

        # Formulario
        ttk.Label(form, text="Código:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        ttk.Entry(form, textvariable=codigo_var).grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)

        ttk.Label(form, text="Nombre:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        ttk.Entry(form, textvariable=nombre_var).grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)

        ttk.Label(form, text="Marca:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        ttk.Entry(form, textvariable=marca_var).grid(row=2, column=1, padx=5, pady=5, sticky=tk.EW)

        ttk.Label(form, text="Modelo:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)
        ttk.Entry(form, textvariable=modelo_var).grid(row=3, column=1, padx=5, pady=5, sticky=tk.EW)

        ttk.Label(form, text="Precio:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.E)
        ttk.Entry(form, textvariable=precio_var).grid(row=4, column=1, padx=5, pady=5, sticky=tk.EW)

        ttk.Label(form, text="Stock:").grid(row=5, column=0, padx=5, pady=5, sticky=tk.E)
        ttk.Entry(form, textvariable=stock_var).grid(row=5, column=1, padx=5, pady=5, sticky=tk.EW)

        ttk.Label(form, text="Categoría:").grid(row=6, column=0, padx=5, pady=5, sticky=tk.E)
        categoria_cb = ttk.Combobox(
            form, 
            textvariable=categoria_var,
            values=[cat['nombre'] for cat in self.categorias]
        )
        categoria_cb.grid(row=6, column=1, padx=5, pady=5, sticky=tk.EW)

        if producto and producto['categoria_id']:
            categoria_cb.current([cat['id'] for cat in self.categorias].index(producto['categoria_id']))

        ttk.Label(form, text="Descripción:").grid(row=7, column=0, padx=5, pady=5, sticky=tk.NE)
        descripcion_txt = tk.Text(form, height=4, width=30)
        descripcion_txt.grid(row=7, column=1, padx=5, pady=5, sticky=tk.EW)
        
        if producto and producto['descripcion']:
            descripcion_txt.insert('1.0', producto['descripcion'])

        # Botones
        btn_frame = ttk.Frame(form)
        btn_frame.grid(row=8, column=0, columnspan=2, pady=10)

        def guardar():
            try:
                categoria_id = self.categorias[categoria_cb.current()]['id'] if categoria_cb.current() >= 0 else None
                
                data = {
                    'codigo': codigo_var.get(),
                    'nombre': nombre_var.get(),
                    'marca': marca_var.get(),
                    'modelo': modelo_var.get(),
                    'precio': float(precio_var.get()),
                    'stock': int(stock_var.get()),
                    'categoria_id': categoria_id,
                    'descripcion': descripcion_txt.get('1.0', tk.END).strip()
                }

                if producto:
                    data['id'] = producto['id']
                    self.producto_controller.actualizar_producto(data)
                    messagebox.showinfo("Éxito", "Producto actualizado correctamente")
                else:
                    self.producto_controller.agregar_producto(data)
                    messagebox.showinfo("Éxito", "Producto agregado correctamente")

                form.destroy()
                self.listar_productos()
            except ValueError as e:
                messagebox.showerror("Error", f"Datos inválidos: {str(e)}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar: {str(e)}")

        ttk.Button(btn_frame, text="Guardar", command=guardar).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancelar", command=form.destroy).pack(side=tk.LEFT, padx=5)

        form.columnconfigure(1, weight=1)

    def editar_producto(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un producto para editar")
            return

        producto_id = self.tree.item(selected[0], 'text')
        producto = self.producto_controller.obtener_producto(producto_id)
        if producto:
            self.abrir_formulario(producto)

    def eliminar_producto(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un producto para eliminar")
            return

        producto_id = self.tree.item(selected[0], 'text')
        
        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este producto?"):
            try:
                self.producto_controller.eliminar_producto(producto_id)
                messagebox.showinfo("Éxito", "Producto eliminado correctamente")
                self.listar_productos()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar: {str(e)}")