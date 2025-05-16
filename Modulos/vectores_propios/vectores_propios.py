import sys
import numpy as np
from fractions import Fraction
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QGridLayout, QTableWidget, QTableWidgetItem, QMessageBox,
    QScrollArea
)
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QRegExpValidator, QDoubleValidator

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class VectoresPropios(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Valores y Vectores Propios")
        self.setGeometry(100, 100, 1200, 700)

        self.layout_principal = QHBoxLayout(self)
        self.setLayout(self.layout_principal)

        # Columna izquierda (entradas)
        self.layout_izquierda = QVBoxLayout()

        # Validador para fracciones y decimales
        self.fraccion_valida = QRegExpValidator(QRegExp(r"^-?\d+(\.\d+)?(/\d+)?$"))

        # Contenedor para todos los inputs
        inputs_layout = QVBoxLayout()

        # Entrada de tamaño de la matriz y botón Crear Matriz
        tamano_layout = QHBoxLayout()
        tamano_layout.addWidget(QLabel("Tamaño de la matriz (n):"))
        self.input_tamano = QLineEdit()
        self.input_tamano.setPlaceholderText("Ej: 3")
        tamano_layout.addWidget(self.input_tamano)
        self.boton_crear = QPushButton("Crear Matriz")
        self.boton_crear.clicked.connect(self.crear_matriz)
        tamano_layout.addWidget(self.boton_crear)
        inputs_layout.addLayout(tamano_layout)

        # Paso (h)
        h_layout = QHBoxLayout()
        h_layout.addWidget(QLabel("Paso h:"))
        self.input_h = QLineEdit()
        self.input_h.setPlaceholderText("Ej: 0.1")
        validator = QDoubleValidator()
        validator.setDecimals(4)
        validator.setBottom(0.0001)
        validator.setNotation(QDoubleValidator.StandardNotation)
        self.input_h.setValidator(validator)
        h_layout.addWidget(self.input_h)
        inputs_layout.addLayout(h_layout)

        # Número de iteraciones (n)
        n_layout = QHBoxLayout()
        n_layout.addWidget(QLabel("Número de iteraciones n:"))
        self.input_n = QLineEdit()
        self.input_n.setPlaceholderText("Ej: 10")
        n_layout.addWidget(self.input_n)
        inputs_layout.addLayout(n_layout)

        self.layout_izquierda.addLayout(inputs_layout)

        # Contenedor para matriz A y x0
        self.matrix_container = QWidget()
        self.matrix_layout = QVBoxLayout(self.matrix_container)
        self.grid_widget = QWidget()
        self.grid_layout = QGridLayout(self.grid_widget)
        self.x0_container = QWidget()
        self.x0_grid_layout = QGridLayout(self.x0_container)
        self.matrix_layout.addWidget(QLabel("Matriz A"))
        self.matrix_layout.addWidget(self.grid_widget)
        self.matrix_layout.addWidget(QLabel("Condiciones iniciales (x0)"))
        self.matrix_layout.addWidget(self.x0_container)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.matrix_container)
        self.layout_izquierda.addWidget(self.scroll_area)

        # Botones
        botones_layout = QHBoxLayout()
        self.boton_calcular = QPushButton("Calcular")
        self.boton_calcular.clicked.connect(self.calcular_valores_vectores)
        self.boton_calcular.setEnabled(False)
        self.boton_limpiar = QPushButton("Limpiar")
        self.boton_limpiar.setStyleSheet("background-color: #ff4757; font-weight: bold; border-radius: 10px; padding: 10px;")
        self.boton_limpiar.clicked.connect(self.limpiar_todo)
        self.boton_volver = QPushButton("Volver")
        self.boton_volver.clicked.connect(self.volver)

        botones_layout.addWidget(self.boton_calcular)
        botones_layout.addWidget(self.boton_limpiar)
        botones_layout.addWidget(self.boton_volver)
        self.layout_izquierda.addLayout(botones_layout)

        self.layout_principal.addLayout(self.layout_izquierda, 1)

        # Columna derecha (tabla de resultados + gráfica)
        self.scroll_resultado = QScrollArea()
        self.scroll_resultado.setWidgetResizable(True)
        self.container_derecho = QWidget()
        self.layout_derecha = QVBoxLayout(self.container_derecho)

        # Tabla de resultados
        self.result_table = QTableWidget()
        self.layout_derecha.addWidget(self.result_table)

        # Gráfica
        self.figure = Figure()
        self.figure.patch.set_facecolor('none')
        self.ax = self.figure.add_subplot(111, projection='3d')
        self.ax.set_facecolor('none')
        self.ax.tick_params(colors='white')
        self.ax.xaxis.label.set_color('white')
        self.ax.yaxis.label.set_color('white')
        self.ax.zaxis.label.set_color('white')
        self.ax.title.set_color('white')

        self.canvas = FigureCanvas(self.figure)
        self.layout_derecha.addWidget(self.canvas)

        self.scroll_resultado.setWidget(self.container_derecho)
        self.layout_principal.addWidget(self.scroll_resultado, 2)

        self.celdas_matriz = []
        self.celdas_x0 = []

    def crear_matriz(self):
        try:
            tamano = int(self.input_tamano.text())
            if tamano <= 0:
                raise ValueError
        except:
            QMessageBox.warning(self, "Entrada inválida", "Introduce un número entero positivo para el tamaño de la matriz.")
            return

        # Limpiar matriz anterior
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        # Limpiar x0 anterior
        for i in reversed(range(self.x0_grid_layout.count())):
            widget = self.x0_grid_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        # Crear entradas para matriz A
        self.celdas_matriz = []
        for i in range(tamano):
            fila = []
            for j in range(tamano):
                celda = QLineEdit("0")
                celda.setFixedSize(150, 150)
                celda.setAlignment(Qt.AlignCenter)
                celda.setValidator(self.fraccion_valida)
                self.grid_layout.addWidget(celda, i, j)
                fila.append(celda)
            self.celdas_matriz.append(fila)

        # Crear entradas para x0
        self.celdas_x0 = []
        for i in range(tamano):
            celda = QLineEdit("0")
            celda.setFixedSize(150, 150)
            celda.setAlignment(Qt.AlignCenter)
            celda.setValidator(self.fraccion_valida)
            self.x0_grid_layout.addWidget(celda, i, 0)
            self.celdas_x0.append([celda])

        self.boton_calcular.setEnabled(True)

    def calcular_valores_vectores(self):
        try:
            # Obtener matriz A
            tamano = len(self.celdas_matriz)
            matriz = np.zeros((tamano, tamano))
            for i in range(tamano):
                for j in range(tamano):
                    texto = self.celdas_matriz[i][j].text()
                    try:
                        valor = float(Fraction(texto))
                        matriz[i][j] = valor
                    except:
                        raise ValueError(f"Valor no válido en la celda ({i+1}, {j+1})")

            # Obtener x0
            x0 = np.zeros((tamano, 1))
            for i in range(tamano):
                texto = self.celdas_x0[i][0].text()
                try:
                    valor = float(Fraction(texto))
                    x0[i, 0] = valor
                except:
                    raise ValueError(f"Valor no válido en x0, posición {i+1}")

            # Obtener h y n
            try:
                h = float(self.input_h.text())
                if h <= 0:
                    raise ValueError
            except:
                raise ValueError("El paso h debe ser un número positivo.")

            try:
                n = int(self.input_n.text())
                if n <= 0:
                    raise ValueError
            except:
                raise ValueError("El número de iteraciones n debe ser un entero positivo.")

            # Calcular valores y vectores propios
            valores, vectores = np.linalg.eig(matriz)

            # Verificar valores propios reales y distintos
            if not np.all(np.isreal(valores)):
                raise ValueError("Este programa solo soporta valores propios reales (no complejos).")
            if len(np.unique(valores)) != len(valores):
                raise ValueError("Este programa solo soporta valores propios distintos (no repetidos).")

            valores = np.real(valores)

            # Resolver para las constantes usando x(0) = x0
            V = vectores
            c = np.linalg.solve(V, x0.flatten())

            # Calcular valores para la tabla
            table_data = []
            for k in range(n + 1):
                t = k * h
                x_t = np.zeros(tamano)
                for i in range(tamano):
                    x_t += c[i] * vectores[:, i] * np.exp(valores[i] * t)
                table_data.append([k, t, x_t])

            # Configurar la tabla
            self.result_table.setRowCount(n + 1)
            self.result_table.setColumnCount(2 + tamano)
            headers = ["Iteración k", "t"] + [f"x_{i+1}" for i in range(tamano)]
            self.result_table.setHorizontalHeaderLabels(headers)

            for row, (k, t, x_t) in enumerate(table_data):
                self.result_table.setItem(row, 0, QTableWidgetItem(f"{k}"))
                self.result_table.setItem(row, 1, QTableWidgetItem(f"{t:.4f}"))
                for i in range(tamano):
                    value = x_t[i]
                    formatted_value = f"{int(value)}" if value == int(value) else f"{value:.4f}"
                    item = QTableWidgetItem(formatted_value)
                    item.setTextAlignment(Qt.AlignCenter)
                    self.result_table.setItem(row, 2 + i, item)

            self.result_table.resizeColumnsToContents()

            # Graficar vectores en 3D
            self.ax.clear()
            self.ax.set_title("Vectores Propios", color='white')
            self.ax.set_xlabel('X', color='white')
            self.ax.set_ylabel('Y', color='white')
            self.ax.set_zlabel('Z', color='white')
            self.ax.set_xlim([-1, 1])
            self.ax.set_ylim([-1, 1])
            self.ax.set_zlim([-1, 1])

            colores = ['r', 'g', 'b', 'c', 'm', 'y', 'k']
            for i in range(min(3, vectores.shape[1])):
                vector = vectores[:, i]
                if len(vector) < 3:
                    vector = np.pad(vector, (0, 3 - len(vector)), mode='constant')
                norma = np.linalg.norm(vector)
                if norma != 0:
                    vector = vector / norma
                color = colores[i % len(colores)]
                self.ax.quiver(0, 0, 0, vector[0], vector[1], vector[2], color=color, arrow_length_ratio=0.3, linewidth=3)

            self.canvas.draw()

        except np.linalg.LinAlgError:
            QMessageBox.critical(self, "Error", "No se pudo resolver el sistema (matriz singular u otro problema numérico).")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error: {str(e)}")

    def limpiar_todo(self):
        self.input_tamano.clear()
        self.input_h.clear()
        self.input_n.clear()
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)
        for i in reversed(range(self.x0_grid_layout.count())):
            widget = self.x0_grid_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)
        self.result_table.setRowCount(0)
        self.result_table.setColumnCount(0)
        self.ax.clear()
        self.canvas.draw()
        self.celdas_matriz = []
        self.celdas_x0 = []
        self.boton_calcular.setEnabled(False)

    def volver(self):
        from Modulos.menu_general.menu_general import MenuGeneral
        self.menu = MenuGeneral()
        self.menu.show()
        self.close()


