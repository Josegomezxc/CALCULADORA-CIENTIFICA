
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

# Se importa re, que es la librería de expresiones regulares para buscar o validar patrones en textos
import re

# Se importa un validador de expresiones regulares para campos de texto en la GUI
from PyQt5.QtGui import QRegularExpressionValidator

# Se importa la clase QRegularExpression para definir patrones de validación
from PyQt5.QtCore import QRegularExpression

from Modulos.menu_general.menu_general import MenuGeneral

from utils.helpers import resource_path
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
        self.boton_calcular.setEnabled(False)
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
            fA = int(self.inputs["Filas A"].text() or 0)
            cA = int(self.inputs["Columnas A"].text() or 0)
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
        self.boton_calcular.setEnabled(True)


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
