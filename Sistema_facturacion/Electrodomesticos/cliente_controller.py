from database.db_connection import DatabaseConnection
from models.cliente import Cliente

class ClienteController:
    def __init__(self):
        self.db = DatabaseConnection()
    
    def agregar_cliente(self, cliente):
        """Agrega un nuevo cliente a la base de datos"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO clientes (tipo_documento, documento, nombres, apellidos, "
                "direccion, telefono, email) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (cliente.tipo_documento, cliente.documento, cliente.nombres, 
                 cliente.apellidos, cliente.direccion, cliente.telefono, cliente.email)
            )
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
    
    def actualizar_cliente(self, cliente):
        """Actualiza un cliente existente"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE clientes SET tipo_documento=%s, documento=%s, nombres=%s, "
                "apellidos=%s, direccion=%s, telefono=%s, email=%s WHERE id=%s",
                (cliente.tipo_documento, cliente.documento, cliente.nombres,
                 cliente.apellidos, cliente.direccion, cliente.telefono, cliente.email, cliente.id)
            )
            conn.commit()
            return cursor.rowcount
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
    
    def eliminar_cliente(self, cliente_id):
        """Elimina un cliente por su ID"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM clientes WHERE id=%s", (cliente_id,))
            conn.commit()
            return cursor.rowcount
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
    
    def obtener_cliente(self, cliente_id):
        """Obtiene un cliente por su ID"""
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM clientes WHERE id=%s", (cliente_id,))
            return cursor.fetchone()
        finally:
            cursor.close()
    
    def buscar_cliente_por_documento(self, documento):
        """Busca un cliente por su número de documento"""
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM clientes WHERE documento=%s", (documento,))
            return cursor.fetchone()
        finally:
            cursor.close()
    
    def listar_clientes(self):
        """Lista todos los clientes"""
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM clientes ORDER BY nombres, apellidos")
            return cursor.fetchall()
        finally:
            cursor.close()
    
    def buscar_clientes(self, criterio):
        """Busca clientes por criterio (documento, nombres o apellidos)"""
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT * FROM clientes WHERE documento LIKE %s OR nombres LIKE %s OR apellidos LIKE %s",
                (f"%{criterio}%", f"%{criterio}%", f"%{criterio}%")
            )
            return cursor.fetchall()
        finally:
            cursor.close()