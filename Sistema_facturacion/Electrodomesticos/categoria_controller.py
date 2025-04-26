from database.db_connection import DatabaseConnection

class CategoriaController:
    def __init__(self):
        self.db = DatabaseConnection()

    def listar_categorias(self):
        """Lista todas las categorías"""
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT id, nombre FROM categorias ORDER BY nombre")
            return cursor.fetchall()
        finally:
            cursor.close()
