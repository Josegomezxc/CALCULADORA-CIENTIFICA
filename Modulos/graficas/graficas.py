
# Importa numpy, una librería para trabajar con arrays y operaciones matemáticas
import numpy as np

from PyQt5.QtWidgets import *  # También importa todos los widgets

# Se importan componentes del núcleo de PyQt5, como señales personalizadas y alineación
from PyQt5.QtCore import Qt
# Se importa sympy, una librería para matemáticas simbólicas (por ejemplo, derivadas, integrales, ecuaciones)
import sympy as sp

# Se importa re, que es la librería de expresiones regulares para buscar o validar patrones en textos
import re

# Se importa FigureCanvas para integrar gráficos de matplotlib en una aplicación PyQt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# Se importa la clase Figure para crear figuras personalizadas de matplotlib
from matplotlib.figure import Figure

from Modulos.menu_general.menu_general import MenuGeneral



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

