# Importaciones necesarias para la interfaz y manejo visual
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

from Modulos.menu_general.menu_general import MenuGeneral
from utils.helpers import resource_path

# Clase del menú de estadística
class MenuEstadistica(QWidget):
    # Constructor de la clase
    def __init__(self):
        super().__init__()
        # Configura el título, tamaño y estilo de la ventana
        self.setWindowTitle("📊 Módulo de Estadística")
        self.setGeometry(100, 100, 900, 600)
        self.setStyleSheet(self.estilos())

        # Diseño principal
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(40, 40, 40, 40)
        layout_principal.setSpacing(30)

        # Título
        titulo = QLabel("📊 Probabilidad y Estadísticas")
        titulo.setObjectName("titulo")
        layout_principal.addWidget(titulo)

        # Cuadrícula de tarjetas para cada operación
        grid = QGridLayout()
        grid.setSpacing(30)
        grid.setAlignment(Qt.AlignCenter)

        # Definición de operaciones estadísticas
        operaciones = [
            ("Num Aleatorios", self.abrir_numeros_aleatorios),
            ("MonteCarlo", self.abrir_montecarlo),
        ]

        # Agregar tarjetas al grid
        row, col = 0, 0
        for texto, funcion in operaciones:
            tarjeta = self.crear_tarjeta(texto, funcion)
            grid.addWidget(tarjeta, row, col)
            col += 1
            if col >= 3:
                row += 1
                col = 0

        layout_principal.addLayout(grid)

        # Botón para volver al menú general
        boton_volver = QPushButton("Volver al menú principal")
        boton_volver.setObjectName("botonVolver")
        boton_volver.setCursor(Qt.PointingHandCursor)
        boton_volver.setFixedWidth(240)
        boton_volver.clicked.connect(self.volver)
        layout_principal.addWidget(boton_volver, alignment=Qt.AlignCenter)

    # Crea tarjetas visuales con imagen y botón para cada operación
    def crear_tarjeta(self, texto, funcion):
        tarjeta = QFrame()
        tarjeta.setObjectName("tarjeta")
        tarjeta.setFixedSize(240, 160)

        layout = QVBoxLayout(tarjeta)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setAlignment(Qt.AlignCenter)

        # Imagen decorativa del módulo
        imagen_label = QLabel()
        ruta_imagen = resource_path(f"images/{texto.lower()}.png")
        pixmap = QPixmap(ruta_imagen).scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        imagen_label.setPixmap(pixmap)
        imagen_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(imagen_label)

        # Botón de la tarjeta
        boton = QPushButton(texto)
        boton.setObjectName("botonTarjeta")
        boton.setCursor(Qt.PointingHandCursor)
        boton.setFixedSize(180, 60)
        boton.clicked.connect(funcion)
        layout.addWidget(boton)

        return tarjeta

    # Estilos visuales personalizados (modo oscuro y moderno)
    def estilos(self):
        return """
        QWidget {
            background-color: #0f111a;
            color: #f1f1f1;
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 15px;
        }

        QLabel#titulo {
            font-size: 30px;
            font-weight: bold;
            padding: 20px;
            background-color: #1a1d2e;
            border-bottom: 3px solid #00d2ff;
            color: #00d2ff;
            qproperty-alignment: AlignCenter;
        }

        QFrame#tarjeta {
            background-color: transparent;
            border-radius: 20px;
            border: 1px solid #2e86de;
        }

        QPushButton#botonTarjeta {
            background-color: qlineargradient(
                x1:0, y1:0, x2:1, y2:1,
                stop:0 #00d2ff,
                stop:1 #3a7bd5
            );
            border: none;
            border-radius: 12px;
            padding: 10px;
            font-size: 16px;
            font-weight: bold;
            color: white;
        }

        QPushButton#botonTarjeta:hover {
            background-color: qlineargradient(
                x1:0, y1:0, x2:1, y2:1,
                stop:0 #3a7bd5,
                stop:1 #00d2ff
            );
            border: 2px solid #00d2ff;
        }

        QPushButton#botonVolver {
            background-color: transparent;
            color: #00d2ff;
            font-size: 15px;
            border: 1px solid #00d2ff;
            padding: 10px 20px;
            border-radius: 12px;
        }

        QPushButton#botonVolver:hover {
            background-color: #1a1d2e;
        }
        """

    # Métodos para abrir cada ventana correspondiente a cada operación
    def abrir_numeros_aleatorios(self):
        from Modulos.estadistica.numeros_aleatorios.numeros_aleatorios import NumerosAleatorios 
        self.ventana = NumerosAleatorios()
        self.ventana.show()
        self.close()
        
    def abrir_montecarlo(self):
        from Modulos.estadistica.montecarlo.montecarlo import MonteCarlo 
        self.ventana = MonteCarlo()
        self.ventana.show()
        self.close()

    def volver(self):
        self.menu = MenuGeneral()
        self.menu.show()
        self.close()
