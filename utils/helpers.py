# Función que obtiene la ruta absoluta de un recurso, útil si se empaqueta la app con PyInstaller
import os
import sys


def resource_path(relative_path): 
    try:
        # Si la app está empaquetada con PyInstaller, usa esta ruta especial
        base_path = sys._MEIPASS  
    except Exception:
        # Si está en desarrollo (no empaquetada), usa la ruta actual del proyecto
        base_path = os.path.abspath(".")
    # Devuelve la ruta completa al archivo o recurso
    return os.path.join(base_path, relative_path)

