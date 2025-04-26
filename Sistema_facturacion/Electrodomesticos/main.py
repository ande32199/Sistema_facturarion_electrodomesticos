
"""
Sistema de Facturación de Electrodomésticos - Punto de entrada principal

Este archivo inicia la aplicación principal del sistema de facturación.
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

# Ajustar sys.path para incluir el directorio padre y permitir importaciones absolutas
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from views.main_window import MainWindow
from database.db_connection import DatabaseConnection

def check_database_connection():
    """Verifica la conexión a la base de datos antes de iniciar la aplicación"""
    try:
        db = DatabaseConnection()
        conn = db.get_connection()
        if conn.is_connected():
            print("Conexión a la base de datos establecida correctamente")
            conn.close()
            return True
        return False
    except Exception as e:
        print(f"Error de conexión a la base de datos: {str(e)}")
        return False

def main():
    """Función principal que inicia la aplicación"""
    try:
        # Verificar conexión a la base de datos
        if not check_database_connection():
            messagebox.showerror(
                "Error de Conexión",
                "No se pudo conectar a la base de datos. Verifique la configuración."
            )
            return

        # Crear y ejecutar la aplicación principal
        app = MainWindow()
        
        # Configurar el manejo de excepciones no capturadas
        def handle_exception(exc_type, exc_value, exc_traceback):
            messagebox.showerror(
                "Error Inesperado",
                f"Ocurrió un error inesperado:\n\n{str(exc_value)}"
            )
        
        # Configurar el manejador de excepciones global
        tk.Tk.report_callback_exception = handle_exception
        
        app.mainloop()
        
    except ImportError as e:
        messagebox.showerror(
            "Error de Importación",
            f"No se pudo importar un módulo requerido:\n\n{str(e)}\n\n"
            "Asegúrese de haber instalado todas las dependencias."
        )
    except Exception as e:
        messagebox.showerror(
            "Error Inicial",
            f"Ocurrió un error al iniciar la aplicación:\n\n{str(e)}"
        )

if __name__ == "__main__":
    # Configuración inicial recomendada para tkinter
    tk.Tk().withdraw()  # Ocultar ventana temporal
    
    # Mostrar mensaje de inicio
    print("Iniciando Sistema de Facturación de Electrodomésticos...")
    
    # Ejecutar la aplicación principal
    main()
