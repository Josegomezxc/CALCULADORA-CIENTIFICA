
from PyQt5.QtWidgets import *  # También importa todos los widgets

# Se importan componentes del núcleo de PyQt5, como señales personalizadas y alineación
from PyQt5.QtCore import Qt

# Se importa QPixmap para mostrar imágenes en la GUI
from PyQt5.QtGui import QPixmap

# from app import AcercaDe, CalculoSimbolico, Graficas_2d_3d, MenuMatrices, MenuPolinomios
from utils.helpers import resource_path

# Diseñar una interfaz gráfica amigable e intuitiva, con un menú principal que
# permita acceder fácilmente a cada módulo de operación.
# Esta clase define el menú principal de una calculadora científica con interfaz gráfica amigable
class MenuGeneral(QWidget):
    # Constructor de la clase, inicializa la ventana
    def __init__(self):
        super().__init__()
        
        # Configura el título, tamaño y estilo de la ventana principal
        self.setWindowTitle("🧠 Calculadora Científica")
        self.setGeometry(100, 100, 900, 600)
        self.setStyleSheet(self.estilos())

        # Crea el diseño principal vertical (de arriba hacia abajo)
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(40, 40, 40, 40)
        layout_principal.setSpacing(30)

        # Agrega el título como etiqueta
        titulo = QLabel("🧠 Calculadora Científica")
        titulo.setObjectName("titulo")  # Se usará en los estilos (CSS)
        layout_principal.addWidget(titulo)

        # Crea una cuadrícula para mostrar botones de los módulos
        grid = QGridLayout()
        grid.setSpacing(30)
        grid.setAlignment(Qt.AlignCenter)

        # Lista de módulos con el texto del botón y la función que se ejecuta al hacer clic
        modulos = [
            ("Matrices", self.abrir_matrices),
            ("Polinomios", self.abrir_polinomios),
            ("Derivadas", self.abrir_derivadas),
            ("Vectores", self.abrir_vectores),
            ("Gráficas", self.abrir_graficas),
            ("EDOs", self.abrir_edo),
            ("Acerca De", self.abrir_acercade),
        ]

        # Organiza las tarjetas en filas y columnas (3 por fila)
        row, col = 0, 0
        for texto, funcion in modulos:
            tarjeta = self.crear_tarjeta(texto, funcion)
            grid.addWidget(tarjeta, row, col)
            col += 1
            if col >= 3:
                row += 1
                col = 0

        layout_principal.addLayout(grid)

        # Botón para salir de la aplicación
        boton_salir = QPushButton("Salir")
        boton_salir.setObjectName("botonVolver")
        boton_salir.setFixedWidth(240)
        boton_salir.setCursor(Qt.PointingHandCursor)
        boton_salir.clicked.connect(QApplication.quit)
        layout_principal.addWidget(boton_salir, alignment=Qt.AlignCenter)


        # Crea una tarjeta visual con una imagen y un botón para cada módulo
    def crear_tarjeta(self, texto, funcion):
        tarjeta = QFrame()
        tarjeta.setObjectName("tarjeta")
        tarjeta.setFixedSize(240, 160)

        layout = QVBoxLayout(tarjeta)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignCenter)

        # Imagen que representa al módulo (se busca en la carpeta 'images/')
        imagen_label = QLabel()
        ruta_imagen = resource_path(f"images/{texto.lower()}.png")
        pixmap = QPixmap(ruta_imagen).scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        imagen_label.setPixmap(pixmap)
        imagen_label.setAlignment(Qt.AlignCenter)
        
        # Botón del módulo
        boton = QPushButton(texto)
        boton.setObjectName("botonTarjeta")
        boton.setCursor(Qt.PointingHandCursor)
        boton.setFixedSize(180, 60)
        boton.clicked.connect(funcion)

        # Añade la imagen y el botón al diseño de la tarjeta
        layout.addWidget(imagen_label)
        layout.addSpacing(10)
        layout.addWidget(boton)
        return tarjeta


    # Devuelve una cadena con estilos CSS personalizados para la interfaz
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

# Cada función abre una nueva ventana específica para cada módulo y cierra el menú principal
    def abrir_matrices(self):
        from Modulos.matrices.matrices import MenuMatrices 
        self.ventana = MenuMatrices()
        self.ventana.show()
        self.close()

    def abrir_polinomios(self):
        from Modulos.polinomios.polinomios import MenuPolinomios
        self.ventana = MenuPolinomios()
        self.ventana.show()
        self.close()

    def abrir_derivadas(self):
        from Modulos.calculo_simbolico.calculosimbolico import CalculoSimbolico
        self.ventana = CalculoSimbolico()
        self.ventana.show()
        self.close()

    def abrir_vectores(self):
        from Modulos.vectores.vectores import MenuVectores
        self.ventana = MenuVectores()
        self.ventana.show()
        self.close()

    def abrir_graficas(self):
        from Modulos.graficas.graficas import Graficas_2d_3d
        self.ventana = Graficas_2d_3d()
        self.ventana.show()
        self.close()
        
    def abrir_edo(self):
        from Modulos.EDO.EDO import EDO
        self.ventana = EDO()
        self.ventana.show()
        self.close()
        
    def abrir_acercade(self):
        from Modulos.acerca_de.acercade import AcercaDe
        self.ventana = AcercaDe()
        self.ventana.show()
        self.close()

