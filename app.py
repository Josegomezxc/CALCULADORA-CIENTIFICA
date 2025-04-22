# Importa el módulo math para operaciones matemáticas básicas como raíces, potencias, etc.
import math

# Módulo para trabajar con rutas y archivos del sistema operativo
import os

# Proporciona acceso a variables y funciones del sistema
import sys

# Importa la librería para graficar
from matplotlib import pyplot as plt

# Importa numpy, una librería para trabajar con arrays y operaciones matemáticas
import numpy as np

# De numpy, se importa la función para invertir matrices (inv), calcular el determinante (det)
# y para manejar errores al trabajar con álgebra lineal (LinAlgError)
from numpy.linalg import inv, det, LinAlgError

from PyQt5.QtWidgets import *  # También importa todos los widgets

# Se importan componentes del núcleo de PyQt5, como señales personalizadas y alineación
from PyQt5.QtCore import Qt, pyqtSignal

# Se importa QPixmap para mostrar imágenes en la GUI
from PyQt5.QtGui import QPixmap

# Se importa sympy, una librería para matemáticas simbólicas (por ejemplo, derivadas, integrales, ecuaciones)
import sympy as sp

# Se importa re, que es la librería de expresiones regulares para buscar o validar patrones en textos
import re

# Se importa FigureCanvas para integrar gráficos de matplotlib en una aplicación PyQt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# Se importa la clase Figure para crear figuras personalizadas de matplotlib
from matplotlib.figure import Figure

# Se importa un validador de expresiones regulares para campos de texto en la GUI
from PyQt5.QtGui import QRegularExpressionValidator

# Se importa la clase QRegularExpression para definir patrones de validación
from PyQt5.QtCore import QRegularExpression

# Función que obtiene la ruta absoluta de un recurso, útil si se empaqueta la app con PyInstaller
def resource_path(relative_path): 
    try:
        # Si la app está empaquetada con PyInstaller, usa esta ruta especial
        base_path = sys._MEIPASS  
    except Exception:
        # Si está en desarrollo (no empaquetada), usa la ruta actual del proyecto
        base_path = os.path.abspath(".")
    # Devuelve la ruta completa al archivo o recurso
    return os.path.join(base_path, relative_path)


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
        self.ventana = MenuMatrices()
        self.ventana.show()
        self.close()

    def abrir_polinomios(self):
        self.ventana = MenuPolinomios()
        self.ventana.show()
        self.close()

    def abrir_derivadas(self):
        self.ventana = CalculoSimbolico()
        self.ventana.show()
        self.close()

    def abrir_vectores(self):
        self.ventana = MenuVectores()
        self.ventana.show()
        self.close()

    def abrir_graficas(self):
        self.ventana = Graficas_2d_3d()
        self.ventana.show()
        self.close()
        
    def abrir_acercade(self):
        self.ventana = AcercaDe()
        self.ventana.show()
        self.close()


# Implementar operaciones básicas y avanzadas con matrices, incluyendo suma,
# resta, multiplicación, determinantes, inversas y resolución de sistemas lineales.
class MenuMatrices(QWidget):
    # Constructor de la clase, inicializa la ventana y establece la operación seleccionada
    def __init__(self):
        super().__init__()
        # Configura el título, tamaño y estilo de la ventana
        self.setWindowTitle("🧮 Calculadora de Matrices")
        self.setGeometry(100, 100, 900, 600)
        self.setStyleSheet(self.estilos())
        # Crea el diseño principal vertical (de arriba hacia abajo)
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(40, 40, 40, 40)
        layout_principal.setSpacing(30)

        # Título
        titulo = QLabel("🧮 Operaciones con Matrices")
        titulo.setObjectName("titulo")
        layout_principal.addWidget(titulo)

        # Crea una cuadrícula para mostrar botones de los módulos
        grid = QGridLayout()
        grid.setSpacing(30)
        grid.setAlignment(Qt.AlignCenter)
        
        # Definición de operaciones que se pueden realizar en las matrices
        operaciones = [
            ("Sumar", self.abrir_suma),
            ("Restar", self.abrir_resta),
            ("Multiplicar", self.abrir_multiplicacion),
            ("Inversa", self.abrir_inversa),
            ("Determinante", self.abrir_determinante),
            ("Sistemas Lineales", self.abrir_Sistemas_Lineales),
        ]

        # Organizar las operaciones en un layout de 3 columnas
        row, col = 0, 0
        for texto, funcion in operaciones:
            tarjeta = self.crear_tarjeta(texto, funcion)
            grid.addWidget(tarjeta, row, col)
            col += 1
            if col >= 3:
                row += 1
                col = 0

        layout_principal.addLayout(grid)

        # Botón volver
        boton_volver = QPushButton("Volver al menú principal")
        boton_volver.setObjectName("botonVolver")
        boton_volver.setCursor(Qt.PointingHandCursor)
        boton_volver.setFixedWidth(240)
        boton_volver.clicked.connect(self.volver)
        layout_principal.addWidget(boton_volver, alignment=Qt.AlignCenter)

    # Crea una tarjeta visual con una imagen y un botón para cada módulo
    def crear_tarjeta(self, texto, funcion):
        tarjeta = QFrame()
        tarjeta.setObjectName("tarjeta")
        tarjeta.setFixedSize(240, 160)

        layout = QVBoxLayout(tarjeta)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setAlignment(Qt.AlignCenter)

        # Imagen correspondiente al módulo
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

    # Cada función abre una nueva ventana específica para cada operación
    def abrir_suma(self):
        self.abrir_operacion("Sumar")

    def abrir_resta(self):
        self.abrir_operacion("Restar")

    def abrir_multiplicacion(self):
        self.abrir_operacion("Multiplicar")

    def abrir_inversa(self):
        self.abrir_operacion("Inversa")

    def abrir_determinante(self):
        self.abrir_operacion("Determinante")
        
    def abrir_Sistemas_Lineales(self):
        self.ecuaciones = SistemasLineales()
        self.ecuaciones.show()
        self.close()

    def abrir_operacion(self, operacion):
        self.ventana = CalculadoraMatrices(operacion)
        self.ventana.show()
        self.close()

    def volver(self):
        self.menu = MenuGeneral()
        self.menu.show()
        self.close()

class CalculadoraMatrices(QWidget):
    # Constructor de la clase, se ejecuta cuando se crea la ventana
    def __init__(self, operacion):
        super().__init__()
        self.operacion = operacion  # Guarda qué operación se va a realizar (suma, resta, etc.)
        self.setWindowTitle(f"Operación: {self.operacion}")  # Título de la ventana
        self.setGeometry(100, 100, 900, 600)  # Tamaño y posición de la ventana

        # Layout vertical principal donde se agregarán los elementos (widgets)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        # Etiqueta que muestra la operación elegida
        self.layout.addWidget(QLabel(f"Operación seleccionada: {self.operacion}"))

        # Layout para pedir dimensiones de las matrices
        self.dim_layout = QGridLayout()
        self.inputs = {}  # Diccionario para guardar los campos de entrada
        etiquetas = ["Filas A", "Columnas A"]  # Etiquetas para la primera matriz
        if self.operacion not in ["Inversa", "Determinante"]:
            etiquetas += ["Filas B", "Columnas B"]  # Si se necesita una segunda matriz

        # Crea los campos de entrada para las dimensiones
        for i, texto in enumerate(etiquetas):
            label = QLabel(texto)
            entrada = QLineEdit()
            self.dim_layout.addWidget(label, 0, i)
            self.dim_layout.addWidget(entrada, 1, i)
            self.inputs[texto] = entrada

        self.layout.addLayout(self.dim_layout)

        # Botón para crear las matrices con las dimensiones introducidas
        self.boton_crear = QPushButton("Crear matrices")
        self.boton_crear.clicked.connect(self.crear_matrices)
        self.layout.addWidget(self.boton_crear)

        # Área donde se mostrarán las matrices con scroll por si son grandes
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_widget = QWidget()
        self.grid_layout = QHBoxLayout()
        self.scroll_widget.setLayout(self.grid_layout)
        self.scroll_area.setWidget(self.scroll_widget)
        self.layout.addWidget(self.scroll_area, stretch=1)

        # Campo de texto para mostrar el resultado
        self.resultado = QTextEdit()
        self.resultado.setReadOnly(True)  # Solo lectura
        self.resultado.setStyleSheet("""  
            font-size: 20px;
            color: #00d2ff;
            background-color: #1a1d2e;
            border: 1px solid #00d2ff;
            border-radius: 10px;
            padding: 10px;
        """)
        self.layout.addWidget(QLabel("Resultado:"))
        self.layout.addWidget(self.resultado)

        # Botones para calcular, limpiar y volver
        botones_layout = QHBoxLayout()
        self.boton_calcular = QPushButton("Calcular")
        self.boton_calcular.clicked.connect(self.calcular)
        self.boton_limpiar = QPushButton("Limpiar")
        self.boton_limpiar.clicked.connect(self.limpiar_campos)
        self.boton_volver = QPushButton("Volver al menú")
        self.boton_volver.clicked.connect(self.volver_al_menu)

        botones_layout.addWidget(self.boton_calcular)
        botones_layout.addWidget(self.boton_limpiar)
        botones_layout.addWidget(self.boton_volver)
        self.layout.addLayout(botones_layout)

    def crear_matrices(self):
        try:
            # Se obtienen las dimensiones desde los campos de entrada
            fA = int(self.inputs["Filas A"].text())
            cA = int(self.inputs["Columnas A"].text())
            fB = int(self.inputs.get("Filas B", QLineEdit()).text() or 0)
            cB = int(self.inputs.get("Columnas B", QLineEdit()).text() or 0)
        except:
            # Si hay error en la entrada, se muestra advertencia
            QMessageBox.warning(self, "Error", "Por favor, ingresa dimensiones válidas.")
            return
        
        # Validador para que solo se puedan escribir fracciones o enteros
        fraccion_valida = QRegularExpressionValidator(QRegularExpression(r"^-?\d+(\/\d+)?$"))

        # Validaciones según la operación
        if self.operacion in ["Sumar", "Restar"]:
            if fA != fB or cA != cB:
                QMessageBox.warning(self, "Error", "Para sumar o restar, las matrices deben tener la misma dimensión.")
                return
        elif self.operacion == "Multiplicar":
            if cA != fB:
                QMessageBox.warning(self, "Error", "Para multiplicar, las columnas de A deben ser iguales a las filas de B.")
                return
        elif self.operacion in ["Inversa", "Determinante"]:
            if fA != cA:
                QMessageBox.warning(self, "Error", "La matriz debe ser cuadrada.")
                return

        # Limpia cualquier matriz creada anteriormente
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        self.entradas_m1 = []  # Lista para guardar entradas de la matriz A
        self.entradas_m2 = []  # Lista para guardar entradas de la matriz B

        # Crear la matriz A
        group_a = QGroupBox("Matriz A")
        grid_a = QGridLayout()
        grid_a.setSpacing(0)
        group_a.setLayout(grid_a)

        for i in range(fA):
            fila = []
            for j in range(cA):
                celda = QLineEdit("0")
                celda.setFixedSize(140, 72)
                celda.setAlignment(Qt.AlignCenter)
                celda.setValidator(fraccion_valida)  
                grid_a.addWidget(celda, i, j)
                fila.append(celda)
            self.entradas_m1.append(fila)

        self.grid_layout.addWidget(group_a)

        # Crear matriz B si la operación lo requiere
        if self.operacion not in ["Inversa", "Determinante"]:
            group_b = QGroupBox("Matriz B")
            grid_b = QGridLayout()
            grid_b.setSpacing(0)
            group_b.setLayout(grid_b)

            for i in range(fB):
                fila = []
                for j in range(cB):
                    celda = QLineEdit("0")
                    celda.setFixedSize(140, 72)
                    celda.setAlignment(Qt.AlignCenter)
                    celda.setValidator(fraccion_valida)  
                    grid_b.addWidget(celda, i, j)
                    fila.append(celda)
                self.entradas_m2.append(fila)

            self.grid_layout.addSpacing(30)  # Espacio entre matrices
            self.grid_layout.addWidget(group_b)

    def obtener_matriz(self, entradas, filas, columnas):
        # Convierte los valores de las celdas en una matriz numérica
        matriz = []
        for i in range(filas):
            fila = []
            for j in range(columnas):
                texto = entradas[i][j].text()
                try:
                    # Si es fracción, la convierte
                    if "/" in texto:
                        num, den = texto.split("/")
                        fila.append(float(num) / float(den))
                    else:
                        fila.append(float(texto))  # Convierte a número decimal
                except:
                    fila.append(0.0)  # Si hay error, coloca 0
            matriz.append(fila)
        return np.array(matriz)  # Convierte a matriz de NumPy

    def calcular(self):
        try:
            # Obtiene nuevamente las dimensiones
            fA = int(self.inputs["Filas A"].text())
            cA = int(self.inputs["Columnas A"].text())
            fB = int(self.inputs.get("Filas B", QLineEdit()).text() or 0)
            cB = int(self.inputs.get("Columnas B", QLineEdit()).text() or 0)
        except:
            QMessageBox.warning(self, "Error", "Dimensiones inválidas.")
            return

        # Obtiene las matrices en forma numérica
        M1 = self.obtener_matriz(self.entradas_m1, fA, cA)
        M2 = self.obtener_matriz(self.entradas_m2, fB, cB) if self.operacion not in ["Inversa", "Determinante"] else None

        try:
            # Realiza la operación seleccionada
            if self.operacion == "Sumar":
                resultado = M1 + M2
            elif self.operacion == "Restar":
                resultado = M1 - M2
            elif self.operacion == "Multiplicar":
                resultado = np.dot(M1, M2)
            elif self.operacion == "Inversa":
                if np.isclose(det(M1), 0):
                    raise ValueError("La matriz no tiene inversa porque su determinante es 0.")
                resultado = inv(M1)
            elif self.operacion == "Determinante":
                resultado = det(M1)
        
        # Manejadores de errores
        except LinAlgError:
            QMessageBox.critical(self, "Error", "La operación no pudo realizarse debido a un problema con la matriz (probablemente no es invertible o tiene un problema estructural).")
            return
        except ValueError as ve:
            QMessageBox.critical(self, "Error", str(ve))
            return
        except Exception:
            QMessageBox.critical(self, "Error", "Ocurrió un error inesperado al calcular la operación.")
            return

        # Muestra el resultado en pantalla
        self.resultado.setText(str(resultado))

    def limpiar_campos(self):
        # Limpia las celdas de ambas matrices
        for fila in getattr(self, 'entradas_m1', []):
            for celda in fila:
                celda.setText("0")
        for fila in getattr(self, 'entradas_m2', []):
            for celda in fila:
                celda.setText("0")
        self.resultado.clear()  # Borra el resultado

    def volver_al_menu(self):
        # Cierra la ventana actual y vuelve al menú principal
        self.menu = MenuMatrices()
        self.menu.show()
        self.close()

# Función que limpia un número en texto (quita espacios y corrige signos)
def limpiar_numero(texto):
    texto = texto.strip()
    texto = re.sub(r'-{2,}', '-', texto)
    if texto.count('-') > 1:
        texto = texto.replace('-', '')
        texto = '-' + texto
    return texto

class SistemasLineales(QWidget):
    volver_menu = pyqtSignal()  # Señal personalizada para volver al menú principal

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Resolver sistema de ecuaciones lineales")  # Título de la ventana
        self.setGeometry(100, 100, 800, 600)  # Tamaño y posición de la ventana

        layout = QVBoxLayout()  # Layout vertical principal
        self.setLayout(layout)

        # Texto de instrucciones para el usuario
        self.instrucciones = QLabel("Escribe un sistema de ecuaciones lineales (una por línea):")
        layout.addWidget(self.instrucciones)

        # Editor de texto donde se escriben las ecuaciones
        self.editor_ecuaciones = QTextEdit()
        self.editor_ecuaciones.setPlaceholderText(
            "Ejemplo:\nx - 3y + 2z = -3\n5x + 6y - z = 13\n4x - y + 3z = 8"
        )
        layout.addWidget(self.editor_ecuaciones)

        # Botón para resolver el sistema
        self.boton_resolver = QPushButton("Resolver sistema")
        self.boton_resolver.clicked.connect(self.resolver)
        layout.addWidget(self.boton_resolver)

        # Etiqueta para mostrar el resultado
        layout.addWidget(QLabel("Resultado:"))

        # Área de texto donde se muestra el resultado
        self.resultado = QTextEdit()
        self.resultado.setReadOnly(True)
        layout.addWidget(self.resultado)

        # Layout horizontal para los botones extra
        botones_extras = QHBoxLayout()

        # Botón para limpiar campos
        self.boton_limpiar = QPushButton("Limpiar")
        self.boton_limpiar.clicked.connect(self.limpiar_campos)
        botones_extras.addWidget(self.boton_limpiar)

        # Botón para volver al menú
        self.boton_volver = QPushButton("Volver al menú")
        self.boton_volver.clicked.connect(self.volver_al_menu)
        botones_extras.addWidget(self.boton_volver)

        # Añadimos los botones al layout principal
        layout.addLayout(botones_extras)

    def limpiar_campos(self):
        # Limpia tanto el área de ecuaciones como el resultado
        self.editor_ecuaciones.clear()
        self.resultado.clear()
        
    def volver_al_menu(self):
        # Cierra esta ventana y vuelve al menú principal
        self.menu = MenuMatrices()
        self.menu.show()
        self.close()

    def analizar_sistema(self, texto):
        # Convierte el texto del sistema en matrices A y B y extrae las variables
        lineas = texto.strip().split('\n')  # Separa línea por línea
        variables = sorted(list(set(re.findall(r'[a-zA-Z]', texto))))  # Detecta todas las letras (variables)
        A = []
        B = []

        for linea in lineas:
            coeficientes = [0] * len(variables)

            izquierda, derecha = linea.split('=')  # Divide en izquierda y derecha del igual
            izquierda = izquierda.replace(' ', '')  # Elimina espacios

            # Encuentra todos los términos con variable en la izquierda
            terminos = re.findall(r'[\+\-]?\d*\.?\d*[a-zA-Z]|\d+/\d+', izquierda)

            for termino in terminos:
                match = re.match(r'([\+\-]?\d*\.?\d*)([a-zA-Z])', termino)
                if match:
                    coef_str, var = match.groups()
                    if coef_str in ['', '+', '-']:
                        coef_str += '1'  # Si el coeficiente es vacío, + o -, asumimos 1 o -1
                    coef = self.convertir_fraccion_a_decimal(coef_str)
                    idx = variables.index(var)
                    coeficientes[idx] = coef  # Se asigna el coeficiente a la variable correspondiente

            A.append(coeficientes)  # Agrega la fila a la matriz A
            B.append(float(derecha.strip()))  # Agrega el valor independiente a B
        
        return np.array(A), np.array(B), variables

    def convertir_fraccion_a_decimal(self, texto):
        # Convierte un texto que puede ser fracción o número decimal a float
        if '/' in texto:
            num, den = texto.split('/')
            return float(num) / float(den)
        else:
            return float(texto)

    def resolver_sistema(self, A, B):
        try:
            # Verificamos que A sea cuadrada
            if A.shape[0] != A.shape[1]:
                return "Error: La matriz A no es cuadrada."
            # Verificamos que A y B tengan el mismo número de filas
            if A.shape[0] != B.shape[0]:
                return "Error: Dimensiones incompatibles entre A y B."
            # Se resuelve el sistema de ecuaciones Ax = B
            x = np.linalg.solve(A, B)
            return x
        except np.linalg.LinAlgError as e:
            # Error típico de matrices no invertibles
            return f"Error al resolver el sistema: {e}"
        except Exception as e:
            # Otro tipo de error
            return f"Error inesperado: {e}"

    def resolver(self):
        # Toma el texto del editor y resuelve el sistema
        texto = self.editor_ecuaciones.toPlainText()
        if not texto.strip():
            QMessageBox.warning(self, "Advertencia", "Por favor escribe un sistema de ecuaciones.")
            return

        try:
            A, B, variables = self.analizar_sistema(texto)  # Analiza el texto y genera matrices
            resultado = self.resolver_sistema(A, B)  # Resuelve el sistema

            if isinstance(resultado, str):
                # Si el resultado es un mensaje de error
                self.resultado.setText(resultado)
            else:
                # Muestra cada variable con su valor redondeado
                texto_resultado = "\n".join(f"{var} = {round(valor, 2)}" for var, valor in zip(variables, resultado))
                self.resultado.setText(texto_resultado)
        except Exception:
            QMessageBox.critical(self, "Error", f"Ocurrió un error al analizar el sistema:\nIngrese bien el Sistema de Ecuaciones.")



# Desarrollar funcionalidades para trabajar con polinomios, como suma,
# multiplicación, derivación, integración y evaluación.
class MenuPolinomios(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📈 Calculadora de Polinomios")  # Título de la ventana
        self.setGeometry(100, 100, 900, 600)  # Tamaño y posición de la ventana
        self.setStyleSheet(self.estilos())  # Aplicamos estilos visuales personalizados

        layout_principal = QVBoxLayout(self)  # Layout vertical principal
        layout_principal.setContentsMargins(40, 40, 40, 40)  # Márgenes alrededor
        layout_principal.setSpacing(30)  # Espaciado entre elementos

        # Título principal del menú
        titulo = QLabel("📈 Operaciones con Polinomios")
        titulo.setObjectName("titulo")  # Nombre del objeto para aplicar estilo
        layout_principal.addWidget(titulo)

        # Contenedor de las tarjetas de operaciones (en forma de grilla)
        grid = QGridLayout()
        grid.setSpacing(30)  # Espacio entre tarjetas
        grid.setAlignment(Qt.AlignCenter)  # Centra el contenido del grid

        # Lista de operaciones y sus funciones asociadas
        operaciones = [
            ("Sumar", self.abrir_suma),
            ("Multiplicar", self.abrir_multiplicacion),
            ("Derivadas", self.abrir_derivada),
            ("Integrales", self.abrir_integracion),
            ("Evaluar", self.abrir_evaluacion),
        ]

        row, col = 0, 0  # Posición inicial en el grid
        for texto, funcion in operaciones:
            tarjeta = self.crear_tarjeta(texto, funcion)  # Crear una tarjeta por operación
            grid.addWidget(tarjeta, row, col)  # Agregar la tarjeta al grid
            col += 1
            if col >= 3:  # Cambiar de fila cada 3 columnas
                row += 1
                col = 0

        layout_principal.addLayout(grid)  # Agregar el grid al layout principal

        # Botón para volver al menú principal
        boton_volver = QPushButton("Volver al menú principal")
        boton_volver.setObjectName("botonVolver")  # Estilo personalizado
        boton_volver.setCursor(Qt.PointingHandCursor)  # Cursor de mano al pasar
        boton_volver.setFixedWidth(240)  # Ancho fijo del botón
        boton_volver.clicked.connect(self.volver)  # Acción al hacer clic
        layout_principal.addWidget(boton_volver, alignment=Qt.AlignCenter)

    def crear_tarjeta(self, texto, funcion):
        tarjeta = QFrame()  # Contenedor tipo tarjeta
        tarjeta.setObjectName("tarjeta")  # Para aplicar estilos CSS
        tarjeta.setFixedSize(240, 160)  # Tamaño fijo de cada tarjeta

        layout = QVBoxLayout(tarjeta)  # Layout vertical dentro de la tarjeta
        layout.setContentsMargins(15, 15, 15, 15)  # Márgenes internos
        layout.setAlignment(Qt.AlignCenter)  # Centra el contenido

        # Imagen decorativa de la operación
        imagen_label = QLabel()
        ruta_imagen = resource_path(f"images/{texto.lower()}.png")  # Ruta de la imagen
        pixmap = QPixmap(ruta_imagen).scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        imagen_label.setPixmap(pixmap)
        imagen_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(imagen_label)

        # Botón dentro de la tarjeta
        boton = QPushButton(texto)
        boton.setObjectName("botonTarjeta")  # Estilo visual del botón
        boton.setCursor(Qt.PointingHandCursor)  # Cursor al pasar
        boton.setFixedSize(180, 60)  # Tamaño del botón
        boton.clicked.connect(funcion)  # Acción al hacer clic
        layout.addWidget(boton)

        return tarjeta  # Devuelve la tarjeta creada

    def estilos(self):
        # Estilos CSS personalizados para la interfaz
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

    # Las siguientes funciones abren la calculadora con la operación correspondiente
    def abrir_suma(self):
        self.abrir_operacion("Sumar")

    def abrir_multiplicacion(self):
        self.abrir_operacion("Multiplicar")

    def abrir_derivada(self):
        self.abrir_operacion("Derivadas")

    def abrir_integracion(self):
        self.abrir_operacion("Integrales")

    def abrir_evaluacion(self):
        self.abrir_operacion("Evaluar")

    # Función que abre la ventana correspondiente a la operación seleccionada
    def abrir_operacion(self, operacion):
        self.ventana = CalculadoraPolinomios(operacion)
        self.ventana.show()
        self.close()

    # Función que vuelve al menú principal
    def volver(self):
        self.menu = MenuGeneral()
        self.menu.show()
        self.close()

        
class CalculadoraPolinomios(QWidget):
    def __init__(self, operacion):
        super().__init__()
        self.operacion = operacion  # Se guarda la operación que el usuario seleccionó
        self.setWindowTitle(f"Operación: {self.operacion}")  # Se configura el título de la ventana
        self.setGeometry(100, 100, 900, 600)  # Tamaño y posición de la ventana

        # Layout principal vertical
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Mostrar qué operación fue seleccionada
        self.layout.addWidget(QLabel(f"Operación seleccionada: {self.operacion}"))

        # Campo de entrada para el Polinomio A
        self.polynomial_a_label = QLabel("Polinomio A:")
        self.polynomial_a_input = QLineEdit()
        self.polynomial_a_input.setPlaceholderText("Ejemplo: 3x^2 + 2x + 1")
        self.layout.addWidget(self.polynomial_a_label)
        self.layout.addWidget(self.polynomial_a_input)

        # Campo de entrada para el Polinomio B
        self.polynomial_b_label = QLabel("Polinomio B:")
        self.polynomial_b_input = QLineEdit()
        self.polynomial_b_input.setPlaceholderText("Ejemplo: 3x^2 + 2x + 1 ")

        # Mostrar campo B solo si la operación lo necesita
        if self.operacion in ["Sumar", "Multiplicar"]:
            self.layout.addWidget(self.polynomial_b_label)
            self.layout.addWidget(self.polynomial_b_input)

        # Área para mostrar el resultado (solo lectura)
        self.resultado = QTextEdit()
        self.resultado.setReadOnly(True)
        self.resultado.setStyleSheet("""
            font-size: 20px;
            color: #00d2ff;
            background-color: #1a1d2e;
            border: 1px solid #00d2ff;
            border-radius: 10px;
            padding: 10px;
        """)
        self.layout.addWidget(QLabel("Resultado:"))
        self.layout.addWidget(self.resultado)

        # Botones: Calcular, Limpiar, Volver
        botones_layout = QHBoxLayout()
        self.boton_calcular = QPushButton("Calcular")
        self.boton_calcular.clicked.connect(self.calcular)
        self.boton_limpiar = QPushButton("Limpiar")
        self.boton_limpiar.clicked.connect(self.limpiar_campos)
        self.boton_volver = QPushButton("Volver al menú")
        self.boton_volver.clicked.connect(self.volver_al_menu)

        botones_layout.addWidget(self.boton_calcular)
        botones_layout.addWidget(self.boton_limpiar)
        botones_layout.addWidget(self.boton_volver)
        self.layout.addLayout(botones_layout)

    def calcular(self):
        # Obtener los textos de entrada y convertirlos a minúsculas
        polinomio_a = self.polynomial_a_input.text().strip().lower()
        polinomio_b = self.polynomial_b_input.text().strip().lower()

        # Si las entradas están vacías, se rellenan con "0"
        if not polinomio_a:
            polinomio_a = "0"
            self.polynomial_a_input.setText("0")
        if not polinomio_b:
            polinomio_b = "0"
            self.polynomial_b_input.setText("0")

        # Función para formatear el texto ingresado en un formato que sympy entienda
        def formatear_polinomio(entrada):
            entrada = entrada.replace('^', '**')  # Cambia potencias a formato de Python
            entrada = entrada.lower()
            entrada = re.sub(r'([a-z])(?=[a-z])', r'\1*', entrada)
            entrada = re.sub(r'(\d)([a-z])', r'\1*\2', entrada)
            entrada = re.sub(r'([a-z])(\d)', r'\1*\2', entrada)
            entrada = re.sub(r'([a-z])\(', r'\1*(', entrada)
            return entrada

        # Función para mostrar el resultado en un formato más limpio
        def presentar_polinomio(expr):
            texto = str(expr)
            texto = texto.replace('**', '^')
            texto = re.sub(r'\b1\*', '', texto)
            texto = re.sub(r'(\d)\*([a-z])', r'\1\2', texto)
            texto = texto.replace('*', '')
            return texto

        # Se crean variables simbólicas para todas las letras del abecedario
        letras = 'abcdefghijklmnopqrstuvwxyz'
        variables = sp.symbols(' '.join(letras))
        variables_dict = dict(zip(letras, variables))

        try:
            # Formatear entradas
            entrada_a = formatear_polinomio(polinomio_a if polinomio_a else "0")
            entrada_b = formatear_polinomio(polinomio_b if polinomio_b else "0")

            # Operación: Suma
            if self.operacion == "Sumar":   
                poly_a = sp.Poly(sp.sympify(entrada_a, locals=variables_dict)).as_expr()
                poly_b = sp.Poly(sp.sympify(entrada_b, locals=variables_dict)).as_expr()
                resultado_expr = sp.simplify(poly_a + poly_b)
                resultado_str = presentar_polinomio(resultado_expr)
                self.resultado.setText(f"Resultado:\n{resultado_str}")

            # Operación: Multiplicación
            elif self.operacion == "Multiplicar":
                poly_a = sp.Poly(sp.sympify(entrada_a, locals=variables_dict)).as_expr()
                poly_b = sp.Poly(sp.sympify(entrada_b, locals=variables_dict)).as_expr()
                resultado_expr = sp.simplify(poly_a * poly_b)
                resultado_str = presentar_polinomio(resultado_expr)
                self.resultado.setText(f"Resultado:\n{resultado_str}")

            # Operación: Derivada
            elif self.operacion == "Derivadas":
                var_str, ok = QInputDialog.getText(self, "Variable", "¿Respecto a qué variable quieres derivar? (por ejemplo: x, y, z)")
                if not ok or not var_str.isalpha():
                    QMessageBox.warning(self, "Variable inválida", "Debes ingresar una variable válida (una letra como x, y, z).")
                    return

                variable = variables_dict.get(var_str.strip().lower())
                if variable is None:
                    QMessageBox.warning(self, "Variable inválida", "Variable no reconocida.")
                    return

                poly_a = sp.sympify(entrada_a, locals=variables_dict)
                resultado_expr = sp.diff(poly_a, variable)
                resultado_str = presentar_polinomio(resultado_expr)
                self.resultado.setText(f"Resultado:\n{resultado_str}")

            # Operación: Integral
            elif self.operacion == "Integrales":
                var_str, ok = QInputDialog.getText(self, "Variable", "¿Respecto a qué variable quieres integrar? (por ejemplo: x, y, z)")
                if not ok or not var_str.isalpha():
                    QMessageBox.warning(self, "Variable inválida", "Debes ingresar una variable válida (una letra como x, y, z).")
                    return

                variable = variables_dict.get(var_str.strip().lower())
                if variable is None:
                    QMessageBox.warning(self, "Variable inválida", "Variable no reconocida.")
                    return

                poly_a = sp.sympify(entrada_a, locals=variables_dict)
                resultado_expr = sp.integrate(poly_a, variable)
                resultado_str = presentar_polinomio(resultado_expr) + " + C"  # Se agrega + C al final por ser una integral indefinida
                self.resultado.setText(f"Resultado:\n{resultado_str}")

            # Operación: Evaluación
            elif self.operacion == "Evaluar":
                valor, ok = QInputDialog.getDouble(self, "Evaluar", "¿En qué valor deseas evaluar el polinomio?")
                if ok:
                    x = variables_dict['x']
                    poly_a = sp.sympify(entrada_a, locals=variables_dict)
                    resultado_eval = poly_a.subs(x, valor)
                    resultado_str = presentar_polinomio(resultado_eval)
                    self.resultado.setText(f"Resultado:\n{resultado_str}")
                else:
                    self.resultado.setText("Evaluación cancelada.")

        except Exception as e:
            # Si ocurre un error en el proceso, se muestra un mensaje de advertencia
            self.resultado.setText("Error en el procesamiento del polinomio.\nVerifica la sintaxis.\nEjemplo: 3x^2 + 2x + 1")

    # Limpia todos los campos de entrada y resultado
    def limpiar_campos(self):
        self.polynomial_a_input.clear()
        self.polynomial_b_input.clear()
        self.resultado.clear()

    # Regresa al menú anterior
    def volver_al_menu(self):
        self.menu = MenuPolinomios()
        self.menu.show()
        self.close()



# Programar operaciones con vectores, como suma, resta, magnitud, producto punto
# y producto cruzado.
class MenuVectores(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📐 Calculadora de Vectores")  # Título de la ventana
        self.setGeometry(100, 100, 900, 600)  # Posición y tamaño de la ventana
        self.setStyleSheet(self.estilos())  # Se aplican estilos personalizados

        layout_principal = QVBoxLayout(self)  # Layout vertical principal
        layout_principal.setContentsMargins(40, 40, 40, 40)  # Márgenes exteriores
        layout_principal.setSpacing(30)  # Espaciado entre elementos del layout

        # Título principal de la ventana
        titulo = QLabel("📐 Operaciones con Vectores")
        titulo.setObjectName("titulo")  # ID para aplicar estilo
        layout_principal.addWidget(titulo)

        # Grid que contiene las tarjetas de operaciones
        grid = QGridLayout()
        grid.setSpacing(30)  # Espacio entre tarjetas
        grid.setAlignment(Qt.AlignCenter)  # Centrado del contenido del grid

        # Lista de operaciones disponibles y su función correspondiente
        operaciones = [
            ("Sumar", self.abrir_suma),
            ("Restar", self.abrir_resta),
            ("Producto Punto", self.abrir_producto_punto),
            ("Magnitud", self.abrir_magnitud),
            ("Producto Cruz", self.abrir_producto_cruz),
        ]

        row, col = 0, 0  # Posición inicial del grid
        for texto, funcion in operaciones:
            tarjeta = self.crear_tarjeta(texto, funcion)  # Crear tarjeta para cada operación
            grid.addWidget(tarjeta, row, col)  # Agregar tarjeta al grid
            col += 1
            if col >= 3:  # Cambiar a la siguiente fila cada 3 columnas
                row += 1
                col = 0

        layout_principal.addLayout(grid)  # Añadir el grid al layout principal

        # Botón para volver al menú principal
        boton_volver = QPushButton("Volver al menú principal")
        boton_volver.setObjectName("botonVolver")  # Estilo personalizado
        boton_volver.setCursor(Qt.PointingHandCursor)  # Cursor en forma de mano
        boton_volver.setFixedWidth(240)  # Ancho fijo del botón
        boton_volver.clicked.connect(self.volver)  # Acción al hacer clic
        layout_principal.addWidget(boton_volver, alignment=Qt.AlignCenter)

    def crear_tarjeta(self, texto, funcion):
        tarjeta = QFrame()  # Tarjeta contenedora de imagen + botón
        tarjeta.setObjectName("tarjeta")  # ID para aplicar estilo
        tarjeta.setFixedSize(240, 160)  # Tamaño fijo

        layout = QVBoxLayout(tarjeta)  # Layout vertical dentro de la tarjeta
        layout.setContentsMargins(15, 15, 15, 15)  # Márgenes internos
        layout.setAlignment(Qt.AlignCenter)  # Centrado del contenido

        # Imagen representativa de la operación
        imagen_label = QLabel()
        ruta_imagen = resource_path(f"images/{texto.lower().replace(' ','_')}.png")  # Ruta a la imagen
        pixmap = QPixmap(ruta_imagen).scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        imagen_label.setPixmap(pixmap)
        imagen_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(imagen_label)

        # Botón que representa la operación
        boton = QPushButton(texto)
        boton.setObjectName("botonTarjeta")  # ID para aplicar estilo
        boton.setCursor(Qt.PointingHandCursor)  # Cursor en forma de mano
        boton.setFixedSize(180, 60)  # Tamaño fijo
        boton.clicked.connect(funcion)  # Acción al hacer clic
        layout.addWidget(boton)

        return tarjeta  # Devolver la tarjeta creada

    def estilos(self):
        # Estilos personalizados de la interfaz (colores, bordes, fuentes, etc.)
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

    # Métodos que abren la calculadora para cada operación
    def abrir_suma(self):
        self.abrir_operacion("Sumar")

    def abrir_resta(self):
        self.abrir_operacion("Restar")

    def abrir_producto_punto(self):
        self.abrir_operacion("Producto Punto")

    def abrir_magnitud(self):
        self.abrir_operacion("Magnitud")

    def abrir_producto_cruz(self):
        self.abrir_operacion("Producto Cruz")

    # Método genérico que abre la ventana de cálculo según la operación
    def abrir_operacion(self, operacion):
        self.ventana = CalculadoraVectores(operacion)
        self.ventana.show()
        self.close()

    # Método que regresa al menú principal
    def volver(self):
        self.menu = MenuGeneral()
        self.menu.show()
        self.close()


class CalculadoraVectores(QWidget):
    def __init__(self, operacion):
        super().__init__()
        self.operacion = operacion  # Guarda la operación seleccionada (Suma, Resta, etc.)
        self.setWindowTitle(f"📐 {operacion} de Vectores")  # Título de la ventana
        self.setGeometry(100, 100, 800, 500)  # Tamaño y posición inicial de la ventana
        self.setStyleSheet("background-color: #0f111a; color: white; font-size: 16px;")  # Estilos generales

        layout_principal = QVBoxLayout(self)  # Layout principal vertical
        layout_principal.setContentsMargins(40, 40, 40, 40)  # Márgenes
        layout_principal.setSpacing(20)  # Espaciado entre elementos

        # Título principal
        titulo = QLabel(f"📐 {operacion} de Vectores")
        titulo.setStyleSheet("font-size: 26px; font-weight: bold; color: #00d2ff;")
        titulo.setAlignment(Qt.AlignCenter)
        layout_principal.addWidget(titulo)
        
        # Etiqueta y campo de entrada para el primer vector
        label_vector1 = QLabel("Vector 1:")
        label_vector1.setStyleSheet("font-weight: bold; color: #00d2ff; font-size: 16px;")
        layout_principal.addWidget(label_vector1)

        self.entrada1 = QLineEdit()
        self.entrada1.setPlaceholderText("Ej: 1, 2, 3")  # Texto de ejemplo
        self.entrada1.setStyleSheet("padding: 10px; border-radius: 10px; background-color: #1a1d2e;")
        layout_principal.addWidget(self.entrada1)

        # Si la operación no es Magnitud, también se pide un segundo vector
        if operacion != "Magnitud":
            label_vector2 = QLabel("Vector 2:")
            label_vector2.setStyleSheet("font-weight: bold; color: #00d2ff; font-size: 16px;")
            layout_principal.addWidget(label_vector2)

            self.entrada2 = QLineEdit()
            self.entrada2.setPlaceholderText("Ej: 4, 5, 6")
            self.entrada2.setStyleSheet("padding: 10px; border-radius: 10px; background-color: #1a1d2e;")
            layout_principal.addWidget(self.entrada2)

        # Botón para calcular el resultado
        self.boton_calcular = QPushButton("Calcular")
        self.boton_calcular.setStyleSheet("""
            QPushButton {
                background-color: #00d2ff;
                border: none;
                border-radius: 10px;
                padding: 10px;
                font-weight: bold;
                color: black;
            }
            QPushButton:hover {
                background-color: #3a7bd5;
                color: white;
            }
        """)
        self.boton_calcular.clicked.connect(self.calcular)
        layout_principal.addWidget(self.boton_calcular)

        # Área donde se muestra el resultado
        self.resultado = QLabel("")
        self.resultado.setAlignment(Qt.AlignCenter)
        self.resultado.setWordWrap(True)  # Permite que el texto se ajuste al ancho
        self.resultado.setStyleSheet("font-size: 18px; color: #f1f1f1; padding-top: 20px;")
        layout_principal.addWidget(self.resultado)

        # Botón para volver al menú de vectores
        boton_volver = QPushButton("Volver")
        boton_volver.setStyleSheet("""
            QPushButton {
                color: #00d2ff;
                border: 1px solid #00d2ff;
                border-radius: 10px;
                padding: 8px;
                background-color: transparent;
            }
            QPushButton:hover {
                background-color: #1a1d2e;
            }
        """)
        boton_volver.clicked.connect(self.volver)
        layout_principal.addWidget(boton_volver, alignment=Qt.AlignCenter)
        
    def limpiar_entrada(self, texto):
        # Limpia la entrada del usuario eliminando espacios y comas innecesarias
        texto = re.sub(r'[,\s]+', ',', texto.strip())  # Reemplaza espacios o comas múltiples por una sola coma
        texto = re.sub(r'-+', '-', texto)  # Reemplaza múltiples signos negativos por uno solo
        texto = texto.strip(',')  # Quita comas al principio o final
        return texto

    def calcular(self):
        try:
            # Limpieza de los textos ingresados
            texto1 = self.limpiar_entrada(self.entrada1.text())
            texto2 = self.limpiar_entrada(self.entrada2.text()) if self.operacion != "Magnitud" else ""

            # Convertir los textos a listas de números flotantes
            vector1 = list(map(float, texto1.split(','))) if texto1 else []
            vector2 = list(map(float, texto2.split(','))) if texto2 else []

            # Validar si hay entradas vacías
            if not vector1 and not vector2 and self.operacion != "Magnitud":
                self.resultado.setText("Por favor, ingresa al menos un vector.")
                return
            if not vector1 and self.operacion == "Magnitud":
                self.resultado.setText("Por favor, ingresa un vector.")
                return

            # Rellenar con ceros si uno de los vectores está vacío
            if self.operacion != "Magnitud":
                if not vector1:
                    vector1 = [0.0] * len(vector2)
                    self.entrada1.setText(', '.join(map(str, vector1)))
                elif not vector2:
                    vector2 = [0.0] * len(vector1)
                    self.entrada2.setText(', '.join(map(str, vector2)))

                # Verificar que ambos vectores tengan la misma dimensión
                if self.operacion in ["Sumar", "Restar", "Producto Punto", "Producto Cruz"] and len(vector1) != len(vector2):
                    self.resultado.setText("❌ Los vectores deben tener la misma dimensión.")
                    return

            # Realizar la operación correspondiente
            if self.operacion == "Sumar":
                resultado = [a + b for a, b in zip(vector1, vector2)]
            elif self.operacion == "Restar":
                resultado = [a - b for a, b in zip(vector1, vector2)]
            elif self.operacion == "Producto Punto":
                resultado = sum(a * b for a, b in zip(vector1, vector2))
            elif self.operacion == "Magnitud":
                resultado = round(math.sqrt(sum(a ** 2 for a in vector1)), 4)  # Magnitud (norma del vector)
            elif self.operacion == "Producto Cruz":
                if len(vector1) != 3 or len(vector2) != 3:
                    self.resultado.setText("❌ El producto cruz solo se define en R³.")
                    return
                # Fórmula del producto cruzado
                a1, a2, a3 = vector1
                b1, b2, b3 = vector2
                resultado = [
                    a2 * b3 - a3 * b2,
                    a3 * b1 - a1 * b3,
                    a1 * b2 - a2 * b1
                ]
            else:
                resultado = "❌ Operación no reconocida."  # Si no coincide con ninguna operación válida

            # Mostrar el resultado
            self.resultado.setText(f"✅ Resultado: {resultado}")

        except ValueError:
            # Error al convertir texto a números
            self.resultado.setText("❌ Entrada inválida. Solo se permiten números separados por comas (ej: 1, 2, 3).")

    def volver(self):
        # Volver al menú de vectores
        self.menu_vectores = MenuVectores()
        self.menu_vectores.show()
        self.close()


# Incluir módulos que permitan la derivación e integración de funciones
# matemáticas simbólicamente.
class CalculoSimbolico(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cálculo Simbólico")
        self.setStyleSheet("background-color: #0f111a; color: white; font-size: 16px;")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout(self)

        titulo = QLabel("🧮 Cálculo Simbólico")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 28px; font-weight: bold; color: #00d2ff;")
        layout.addWidget(titulo)

        self.input = QTextEdit()
        self.input.setPlaceholderText("Escribe una función como (3x^3)*sen(x)")
        self.input.setStyleSheet("background-color: #1e1e1e; border: 1px solid #00d2ff; border-radius: 10px;")
        self.input.setFixedHeight(100)
        layout.addWidget(self.input)

        fila = QHBoxLayout()
        self.opciones = QComboBox()
        self.opciones.addItems(["Derivar", "Integrar"])
        self.opciones.setStyleSheet("background-color: #1e1e1e; border: 1px solid #00d2ff;")
        fila.addWidget(self.opciones)

        self.variable_box = QTextEdit()
        self.variable_box.setPlaceholderText("Respecto a")
        self.variable_box.setFixedHeight(40)
        self.variable_box.setFixedWidth(120)
        self.variable_box.setStyleSheet("background-color: #1e1e1e; border: 1px solid #00d2ff;")
        fila.addWidget(self.variable_box)

        self.boton_calcular = QPushButton("Calcular")
        self.boton_calcular.setCursor(Qt.PointingHandCursor)
        self.boton_calcular.setStyleSheet("background-color: #00d2ff; font-weight: bold; border-radius: 10px; padding: 10px;")
        self.boton_calcular.clicked.connect(self.calcular)
        fila.addWidget(self.boton_calcular)
        
        # Botón Limpiar
        self.boton_limpiar = QPushButton("Limpiar")
        self.boton_limpiar.setCursor(Qt.PointingHandCursor)
        self.boton_limpiar.setStyleSheet("background-color: #ff6f61; font-weight: bold; border-radius: 10px; padding: 10px;")
        self.boton_limpiar.clicked.connect(self.limpiar_campos)
        fila.addWidget(self.boton_limpiar)

        # Botón Salir
        self.boton_salir = QPushButton("Salir")
        self.boton_salir.setCursor(Qt.PointingHandCursor)
        self.boton_salir.setStyleSheet("background-color: #ff4757; font-weight: bold; border-radius: 10px; padding: 10px;")
        self.boton_salir.clicked.connect(self.volver)
        fila.addWidget(self.boton_salir)
        layout.addLayout(fila)

        # Resultado
        self.resultado = QLabel("Resultado:")
        self.resultado.setWordWrap(True)
        self.resultado.setStyleSheet("background-color: #1e1e1e; border: 1px solid #00d2ff; padding: 12px; border-radius: 10px;")
        layout.addWidget(self.resultado)

        # Teclado
        self.teclado = self.crear_teclado()
        layout.addLayout(self.teclado)
        
    def limpiar_campos(self):
        self.input.clear()
        self.resultado.setText("Resultado:")
        
    def volver(self):
        self.menu = MenuGeneral()
        self.menu.show()
        self.close()

    def crear_teclado(self):
        teclado_widget = QWidget()
        teclado_layout = QGridLayout(teclado_widget)

        botones = [
            ('1', '1'), ('2', '2'), ('3', '3'), ('+', '+'),
            ('4', '4'), ('5', '5'), ('6', '6'), ('-', '-'),
            ('7', '7'), ('8', '8'), ('9', '9'), ('*', '*'),
            ('0', '0'), ('.', '.'), ('/', '/'), ('^', '**'),
            ('(', '('), (')', ')'), ('log', 'log('), ('exp', 'exp('),
            ('sen', 'sin('), ('cos', 'cos('), ('tan', 'tan('), ('√', 'sqrt('),
            ('π', 'pi'), ('x', 'x'), ('y', 'y'), ('z', 'z')
        ]

        for i, (texto, valor) in enumerate(botones):
            boton = QPushButton(texto)
            boton.setStyleSheet("""
                QPushButton {
                    background-color: #2c2f4a;
                    color: white;
                    font-weight: bold;
                    border-radius: 8px;
                    padding: 15px;
                }
                QPushButton:hover {
                    background-color: #3e4160;
                }
            """)
            boton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            boton.clicked.connect(self.crear_insertador(valor))
            teclado_layout.addWidget(boton, i // 4, i % 4)

        # Envolver en un scroll area para mejor comportamiento en ventanas pequeñas
        scroll_area = QScrollArea()
        scroll_area.setWidget(teclado_widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setStyleSheet("background-color: transparent;")

        # Contenedor de layout final
        teclado_contenedor = QVBoxLayout()
        teclado_contenedor.addWidget(scroll_area)

        return teclado_contenedor



    def crear_insertador(self, valor):
        def insertar():
            cursor = self.input.textCursor()
            cursor.insertText(valor)
        return insertar


    def preprocesar(self, texto):
        texto = texto.replace("^", "**")
        texto = texto.replace("sen", "sin")
        texto = texto.lower()

        funciones = ['sin', 'cos', 'tan', 'exp', 'log', 'sqrt']

        # Proteger funciones para evitar insertar * dentro de ellas
        for f in funciones:
            texto = re.sub(rf'\b{f}\(', f'__{f}__(' , texto)

        # Insertar * entre número y letra o paréntesis (3x → 3*x, 2(x+1) → 2*(x+1))
        texto = re.sub(r'(\d)([a-z\(])', r'\1*\2', texto)

        # Insertar * entre letra y número (x2 → x*2)
        texto = re.sub(r'([a-z])(\d)', r'\1*\2', texto)

        # Insertar * entre letra y paréntesis (x( → x*( )
        texto = re.sub(r'([a-z])\(', r'\1*(', texto)

        # Restaurar funciones protegidas
        for f in funciones:
            texto = texto.replace(f'__{f}__', f)

        return texto




    def calcular(self):
        entrada = self.input.toPlainText().strip().lower()
        variable_str = self.variable_box.toPlainText().strip().lower()

        if not entrada or not variable_str.isalpha():
            QMessageBox.warning(self, "Variable inválida", "Debes ingresar una expresión y una variable válida como x, y, z...")
            return

        try:
            entrada_proc = self.preprocesar(entrada)
            variable = sp.Symbol(variable_str)
            expresion = sp.sympify(entrada_proc)

            if self.opciones.currentText() == "Derivar":
                resultado = sp.diff(expresion, variable)
            else:
                resultado = sp.integrate(expresion, variable)
                resultado = sp.simplify(resultado)
                resultado = sp.expand(resultado)
                resultado = sp.nsimplify(resultado)
                resultado = sp.simplify(resultado)

            resultado_str = presentar_polinomio(resultado)
            if self.opciones.currentText() == "Integrar":
                resultado_str += " + C"

            self.resultado.setText(f"Resultado:\n{resultado_str}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo calcular. Asegúrate de que la expresión esté bien escrita.\n\n{str(e)}")

def presentar_polinomio(expr):
    expr = sp.expand(expr)
    return str(expr).replace("**", "^").replace("*", "")
# Incorporar herramientas de visualización gráfica en 2D y 3D para representar
# funciones de una o más variables.

class Graficas_2d_3d(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gráficas en 2D y 3D")  # Título de la ventana
        self.setStyleSheet("background-color: #0f111a; color: white; font-size: 16px;")  # Estilos globales
        self.setGeometry(100, 100, 1000, 600)  # Tamaño y posición de la ventana

        main_layout = QHBoxLayout(self)  # Layout principal en horizontal

        layout_izquierdo = QVBoxLayout()  # Layout vertical para la parte izquierda

        # Título de la sección de gráficos
        titulo = QLabel("📈 Gráficas en 2D y 3D")
        titulo.setAlignment(Qt.AlignCenter)  # Alineación del título
        titulo.setStyleSheet("font-size: 28px; font-weight: bold; color: #00d2ff;")  # Estilo del título
        layout_izquierdo.addWidget(titulo)

        # Campo de entrada para la función
        self.input_funcion = QLineEdit()
        self.funciones_guardadas = []  # Lista para almacenar funciones 2D ingresadas
        self.input_funcion.setPlaceholderText("Escribe una función(por ejemplo: x**2 * exp(x) o x*exp(-x**2 - y**2))")
        self.input_funcion.setStyleSheet("padding: 10px; border-radius: 8px; background-color: #1c1e2c; color: white;")
        self.input_funcion.textChanged.connect(self.convertir_minusculas)  # Conectar cambio de texto a función
        layout_izquierdo.addWidget(self.input_funcion)

        # Teclado para insertar símbolos y operadores
        teclado_layout = QGridLayout()
        botones = [
            ('1', '1'), ('2', '2'), ('3', '3'), ('/', '/'),
            ('4', '4'), ('5', '5'), ('6', '6'), ('*', '*'),
            ('7', '7'), ('8', '8'), ('9', '9'), ('-', '-'),
            ('0', '0'), ('.', '.'), ('+', '+'), ('^', '**'),
            ('(', '('), (')', ')'), ('log', 'log('), ('exp', 'exp('),
            ('sin', 'sin('), ('cos', 'cos('), ('tan', 'tan('), ('√', 'sqrt('),
            ('x', 'x'), ('y', 'y'), ('π', 'pi')
        ]

        # Crear los botones del teclado y conectarlos a su función respectiva
        for i, (text, value) in enumerate(botones):
            boton = QPushButton(text)
            boton.setStyleSheet("background-color: #2c2f4a; color: white; font-weight: bold; border-radius: 8px; padding: 10px;")
            boton.clicked.connect(self.crear_insertador(value))  # Función de inserción al campo de texto
            teclado_layout.addWidget(boton, i // 4, i % 4)

        layout_izquierdo.addLayout(teclado_layout)

        # Layout para los botones de acción (mostrar gráfica, limpiar, volver)
        botones = QHBoxLayout()

        # Botón para mostrar gráfica 2D
        self.boton_2d = QPushButton("Mostrar gráfica 2D")
        self.boton_2d.setCursor(Qt.PointingHandCursor)
        self.boton_2d.setStyleSheet("background-color: #1e90ff; font-weight: bold; border-radius: 10px; padding: 10px;")
        self.boton_2d.clicked.connect(self.mostrar_grafica_2d)  # Acción al hacer clic
        botones.addWidget(self.boton_2d)

        # Botón para mostrar gráfica 3D
        self.boton_3d = QPushButton("Mostrar gráfica 3D")
        self.boton_3d.setCursor(Qt.PointingHandCursor)
        self.boton_3d.setStyleSheet("background-color: #1e90ff; font-weight: bold; border-radius: 10px; padding: 10px;")
        self.boton_3d.clicked.connect(self.mostrar_grafica_3d)  # Acción al hacer clic
        botones.addWidget(self.boton_3d)

        # Botón para limpiar los campos de entrada y las funciones guardadas
        self.boton_limpiar = QPushButton("Limpiar")
        self.boton_limpiar.setCursor(Qt.PointingHandCursor)
        self.boton_limpiar.setStyleSheet("background-color: #ff4757; font-weight: bold; border-radius: 10px; padding: 10px;")
        self.boton_limpiar.clicked.connect(self.limpiar_campos)  # Acción al hacer clic
        botones.addWidget(self.boton_limpiar)
        
        layout_izquierdo.addLayout(botones)

        # Botón para volver al menú principal
        self.boton_volver = QPushButton("Volver")
        self.boton_volver.setCursor(Qt.PointingHandCursor)
        self.boton_volver.setStyleSheet("background-color: #1e90ff; font-weight: bold; border-radius: 10px; padding: 10px;")
        self.boton_volver.clicked.connect(self.volver)  # Acción al hacer clic
        layout_izquierdo.addWidget(self.boton_volver)

        main_layout.addLayout(layout_izquierdo)

        # Canvas para mostrar los gráficos
        self.figura = Figure(figsize=(5, 4), facecolor='#1c1e2c')  # Crear figura para el gráfico
        self.canvas = FigureCanvas(self.figura)  # Canvas para dibujar en la figura
        main_layout.addWidget(self.canvas)

    # Crea un inserto de texto en el campo de entrada
    def crear_insertador(self, valor):
        def insertar():
            self.input_funcion.insert(valor)  # Inserta el valor correspondiente
        return insertar

    # Convierte el texto en el campo de entrada a minúsculas
    def convertir_minusculas(self, texto):
        cursor_pos = self.input_funcion.cursorPosition()
        self.input_funcion.blockSignals(True)
        self.input_funcion.setText(texto.lower())  # Convierte el texto a minúsculas
        self.input_funcion.setCursorPosition(cursor_pos)
        self.input_funcion.blockSignals(False)

    # Preprocesa la función, reemplazando ciertos símbolos y expresiones
    def preprocesar_funcion(self, expr):
        expr = expr.replace('^', '**')  # Reemplaza el símbolo de potencia
        expr = expr.replace('π', 'pi')  # Reemplaza pi por 'pi' en la expresión
        expr = expr.replace('sen', 'sin')  # Reemplaza 'sen' por 'sin'
        expr = re.sub(r'e\^\(([^()]*)\)', r'exp(\1)', expr)  # Reemplaza e^(...) por exp(...)
        expr = re.sub(r'e\^(-?[a-zA-Z0-9_\*\+\-/\.]+)', r'exp(\1)', expr)  # Reemplaza e^x por exp(x)
        return expr

    # Muestra la gráfica 2D de la función ingresada
    def mostrar_grafica_2d(self):
        expresion_original = self.input_funcion.text()
        expr = self.preprocesar_funcion(expresion_original)

        if 'y' in expr:  # Verifica que no haya una 'y' en la expresión
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Error al graficar 2D")
            msg.setInformativeText("La gráfica 2D solo admite la variable 'x'. Usa 'Mostrar gráfica 3D' si tu expresión incluye 'y'.")
            msg.setWindowTitle("Error")
            msg.exec_()
            return

        x = sp.symbols('x')
        try:
            funcion = sp.sympify(expr)  # Convierte la expresión en una función simbólica
            f = sp.lambdify(x, funcion, 'numpy')  # Convierte la función simbólica a una función de numpy

            # Guardar la función si es válida y no está duplicada
            if expresion_original not in self.funciones_guardadas:
                self.funciones_guardadas.append(expresion_original)

            x_val = np.linspace(-10, 10, 400)  # Rango de valores para x

            self.figura.clear()  # Limpiar la figura antes de graficar
            ax = self.figura.add_subplot(111)  # Crear el eje de la gráfica

            # Graficar todas las funciones almacenadas
            for func_text in self.funciones_guardadas:
                func_expr = self.preprocesar_funcion(func_text)
                func = sp.sympify(func_expr)
                f = sp.lambdify(x, func, 'numpy')
                y_val = f(x_val)
                ax.plot(x_val, y_val, label=f"$y = {func_text}$")

            ax.set_xlabel("x")  # Etiqueta del eje X
            ax.set_ylabel("y")  # Etiqueta del eje Y
            ax.grid(True)
            ax.tick_params(colors='white')  # Color de las marcas del eje
            ax.set_facecolor('#1c1e2c')  # Fondo de la gráfica
            ax.set_title("Funciones graficadas", color="white")  # Título de la gráfica
            ax.legend(loc="upper right", fontsize=9)  # Leyenda
            self.figura.tight_layout()
            self.canvas.draw()  # Dibuja la gráfica en el canvas
        except Exception:
            # Muestra un mensaje de error si algo sale mal
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Error al graficar 2D")
            msg.setInformativeText("Verifica que la expresión sea válida. Usa 'x' como variable.")
            msg.setWindowTitle("Error")
            msg.exec_()

    # Muestra la gráfica 3D de la función ingresada
    def mostrar_grafica_3d(self):
        expresion_original = self.input_funcion.text()
        expr = self.preprocesar_funcion(expresion_original)

        x, y = sp.symbols('x y')
        try:
            funcion = sp.sympify(expr)  # Convierte la expresión en una función simbólica
            f = sp.lambdify((x, y), funcion, 'numpy')  # Convierte la función simbólica a una función de numpy

            x_vals = np.linspace(-5, 5, 100)
            y_vals = np.linspace(-5, 5, 100)
            X, Y = np.meshgrid(x_vals, y_vals)  # Crear la malla de puntos
            Z = f(X, Y)  # Calcular los valores de Z

            self.figura.clear()  # Limpiar la figura
            ax = self.figura.add_subplot(111, projection="3d")  # Crear gráfico 3D
            ax.plot_surface(X, Y, Z, cmap="viridis")  # Mostrar superficie 3D
            ax.set_title(f"$z = {expresion_original}$", color="white")  # Título del gráfico
            ax.set_xlabel("X")  # Etiqueta eje X
            ax.set_ylabel("Y")  # Etiqueta eje Y
            ax.set_zlabel("Z")  # Etiqueta eje Z
            self.figura.tight_layout()
            self.canvas.draw()  # Dibuja la gráfica 3D en el canvas
        except Exception:
            # Muestra un mensaje de error si algo sale mal
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Error al graficar 3D")
            msg.setInformativeText("Verifica que la expresión sea válida. Usa 'x' y 'y' como variables.")
            msg.setWindowTitle("Error")
            msg.exec_()

    # Limpia los campos de entrada y las funciones guardadas
    def limpiar_campos(self):
        self.input_funcion.clear()
        self.funciones_guardadas.clear()  # Limpiar las funciones almacenadas también
        if self.canvas.figure.axes and self.canvas.figure.axes[0].has_data():
            self.canvas.figure.clear()  # Limpiar los gráficos del canvas
            self.canvas.draw()

    # Vuelve al menú principal
    def volver(self):
        self.menu = MenuGeneral()
        self.menu.show()
        self.close()



# Incluir un apartado “Acerca de” dentro del menú principal, que muestre
# información del autor, carrera, semestre, año académico, profesor y materia.
class AcercaDe(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Acerca de")  # Título de la ventana
        self.setGeometry(100, 100, 800, 600)  # Tamaño y posición de la ventana
        self.setStyleSheet("background-color: #0f111a; color: white; font-size: 18px;")  # Estilo de la ventana

        layout = QVBoxLayout()  # Layout principal (vertical)

        # Título de la sección
        titulo = QLabel("📘 Acerca del Proyecto")
        titulo.setAlignment(Qt.AlignCenter)  # Centra el título
        titulo.setStyleSheet("font-size: 30px; font-weight: bold; color: #00d2ff;")  # Estilo del título
        layout.addWidget(titulo)  # Agrega el título al layout

        # Contenido de la sección "Acerca de"
        contenido = QLabel(
            "<b>👨‍💻 Autor:</b> Gómez Molina José Andrés<br><br>"
            "<b>🎓 Carrera:</b> Ingeniería en Software<br><br>"
            "<b>📚 Semestre:</b> 6° Semestre<br><br>"
            "<b>📅 Año Académico:</b> 2025<br><br>"
            "<b>👨‍🏫 Profesor:</b> Ing. Isidro Fabricio Morales Torres<br><br>"
            "<b>🧠 Materia:</b> Modelos Matemáticos y Simulación"
        )

        # Estilo del contenido
        contenido.setStyleSheet("padding: 19px; font-size: 25px;")
        contenido.setAlignment(Qt.AlignLeft | Qt.AlignTop)  # Alineación del contenido a la izquierda y arriba
        contenido.setWordWrap(True)  # Permite que el texto se ajuste en caso de ser largo
        layout.addWidget(contenido)  # Agrega el contenido al layout

        # Botón para volver al menú
        boton_volver = QPushButton("Volver al Menú")
        boton_volver.setCursor(Qt.PointingHandCursor)  # Cambia el cursor a mano al pasar sobre el botón
        boton_volver.setStyleSheet(
            "background-color: #00d2ff; font-weight: bold; border-radius: 10px; padding: 10px; font-size: 18px;"
        )  # Estilo del botón
        boton_volver.clicked.connect(self.volver)  # Conecta el botón con la acción de volver
        layout.addWidget(boton_volver, alignment=Qt.AlignCenter)  # Agrega el botón al layout y lo centra

        # Asigna el layout a la ventana
        self.setLayout(layout)

    # Función para volver al menú general
    def volver(self):
        self.menu = MenuGeneral()  # Crea una instancia del menú principal
        self.menu.show()  # Muestra el menú principal
        self.close()  # Cierra la ventana actual


# Código de ejecución de la aplicación
app = QApplication(sys.argv)

ventana = MenuGeneral()  # Crea una instancia de la ventana del menú general
with open(resource_path("styles.css"), "r") as f:  # Carga los estilos desde un archivo CSS
    stylesheet = f.read()  # Lee los estilos
app.setStyleSheet(stylesheet)  # Aplica los estilos a la aplicación

ventana.show()  # Muestra la ventana del menú general
sys.exit(app.exec_())  # Ejecuta la aplicación

