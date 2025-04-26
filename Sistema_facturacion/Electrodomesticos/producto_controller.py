from database.db_connection import DatabaseConnection
from models.producto import Producto

class ProductoController:
    def __init__(self):
        self.db = DatabaseConnection()
    
    def agregar_producto(self, producto):
        """Agrega un nuevo producto a la base de datos"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO productos (codigo, nombre, marca, modelo, precio, stock, categoria_id, descripcion) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (producto.codigo, producto.nombre, producto.marca, producto.modelo, 
                 producto.precio, producto.stock, producto.categoria_id, producto.descripcion)
            )
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
    
    def actualizar_producto(self, producto):
        """Actualiza un producto existente"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE productos SET codigo=%s, nombre=%s, marca=%s, modelo=%s, "
                "precio=%s, stock=%s, categoria_id=%s, descripcion=%s WHERE id=%s",
                (producto.codigo, producto.nombre, producto.marca, producto.modelo, 
                 producto.precio, producto.stock, producto.categoria_id, producto.descripcion, producto.id)
            )
            conn.commit()
            return cursor.rowcount
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
    
    def eliminar_producto(self, producto_id):
        """Elimina un producto por su ID"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM productos WHERE id=%s", (producto_id,))
            conn.commit()
            return cursor.rowcount
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
    
    def obtener_producto(self, producto_id):
        """Obtiene un producto por su ID"""
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM productos WHERE id=%s", (producto_id,))
            return cursor.fetchone()
        finally:
            cursor.close()
    
    def listar_productos(self):
        """Lista todos los productos"""
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM productos ORDER BY nombre")
            return cursor.fetchall()
        finally:
            cursor.close()
    
    def buscar_productos(self, criterio):
        """Busca productos por criterio (código o nombre)"""
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT * FROM productos WHERE codigo LIKE %s OR nombre LIKE %s",
                (f"%{criterio}%", f"%{criterio}%")
            )
            return cursor.fetchall()
        finally:
            cursor.close()
    
    def actualizar_stock(self, producto_id, cantidad):
        """Actualiza el stock de un producto"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE productos SET stock = stock + %s WHERE id = %s",
                (cantidad, producto_id)
            )
            conn.commit()
            return cursor.rowcount
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()