
# Proporciona acceso a variables y funciones del sistema
import sys

from PyQt5.QtWidgets import *  # También importa todos los widgets

from Modulos.menu_general.menu_general import MenuGeneral
# from Modulos.vectores.vectores import MenuVectores
from utils.helpers import resource_path

# Código de ejecución de la aplicación
app = QApplication(sys.argv)

ventana = MenuGeneral()  # Crea una instancia de la ventana del menú general
with open(resource_path("styles.css"), "r") as f:  # Carga los estilos desde un archivo CSS
    stylesheet = f.read()  # Lee los estilos
app.setStyleSheet(stylesheet)  # Aplica los estilos a la aplicación

ventana.show()  # Muestra la ventana del menú general
sys.exit(app.exec_())  # Ejecuta la aplicación

