from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from sympy import *
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox

from Modulos.menu_general.menu_general import MenuGeneral

class EDO(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Resolución de EDOs")
        self.setStyleSheet("background-color: #0f111a; color: white; font-size: 16px;")
        self.setGeometry(100, 100, 1000, 600)

        layout = QVBoxLayout(self)

        titulo = QLabel("📈 Resolución de EDOs")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 28px; font-weight: bold; color: #00d2ff;")
        layout.addWidget(titulo)

        self.ecuacion_input = QTextEdit()
        self.ecuacion_input.setPlaceholderText("Escribe la EDO como y' = f(x,y)")
        self.ecuacion_input.setStyleSheet("background-color: #1e1e1e; border: 1px solid #00d2ff; border-radius: 10px;")
        self.ecuacion_input.setFixedHeight(80)
        layout.addWidget(self.ecuacion_input)

        parametros_layout = QGridLayout()
        labels = ["x0:", "y0:", "xf:", "h:"]
        self.parametros = {}
        for i, label in enumerate(labels):
            lbl = QLabel(label)
            lbl.setStyleSheet("color: white;")
            parametros_layout.addWidget(lbl, 0, i)
            box = QLineEdit()
            box.setStyleSheet("background-color: #1e1e1e; border: 1px solid #00d2ff; border-radius: 8px; padding: 6px;")
            self.parametros[label] = box
            parametros_layout.addWidget(box, 1, i)

        layout.addLayout(parametros_layout)

        fila_botones = QHBoxLayout()
        self.metodo_combo = QComboBox()
        self.metodo_combo.addItems(["Euler", "Heun", "Runge-Kutta 4", "Taylor"])
        self.metodo_combo.setStyleSheet("background-color: #1e1e1e; border: 1px solid #00d2ff; color: white;")
        fila_botones.addWidget(self.metodo_combo)

        boton_calcular = QPushButton("Calcular")
        boton_calcular.setCursor(Qt.PointingHandCursor)
        boton_calcular.setStyleSheet("background-color: #00d2ff; font-weight: bold; border-radius: 10px; padding: 10px;")
        boton_calcular.clicked.connect(self.calcular)
        fila_botones.addWidget(boton_calcular)

        boton_limpiar = QPushButton("Limpiar")
        boton_limpiar.setCursor(Qt.PointingHandCursor)
        boton_limpiar.setStyleSheet("background-color: #ff6f61; font-weight: bold; border-radius: 10px; padding: 10px;")
        boton_limpiar.clicked.connect(self.limpiar_campos)
        fila_botones.addWidget(boton_limpiar)

        boton_salir = QPushButton("Salir")
        boton_salir.setCursor(Qt.PointingHandCursor)
        boton_salir.setStyleSheet("background-color: #ff4757; font-weight: bold; border-radius: 10px; padding: 10px;")
        boton_salir.clicked.connect(self.volver)
        fila_botones.addWidget(boton_salir)

        layout.addLayout(fila_botones)

        contenido_layout = QHBoxLayout()

        self.canvas = FigureCanvas(plt.figure(facecolor='#0f111a'))
        self.canvas.setFixedWidth(600)
        contenido_layout.addWidget(self.canvas)

        self.tabla = QTableWidget()
        self.tabla.setStyleSheet("background-color: #1e1e1e; border: 1px solid #00d2ff; color: white;")
        self.tabla.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tabla.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tabla.setFixedWidth(240)  # Fija el ancho total de la tabla
        self.tabla.setFixedHeight(310)  # Fija la altura para evitar cambios al añadir datos
        self.tabla.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tabla.setSelectionMode(QAbstractItemView.NoSelection)
        contenido_layout.addWidget(self.tabla)

        layout.addLayout(contenido_layout)

    def limpiar_campos(self):
        self.ecuacion_input.clear()
        for box in self.parametros.values():
            box.clear()
        self.tabla.clear()
        self.canvas.figure.clear()
        self.canvas.draw()

    def volver(self):
        self.menu = MenuGeneral()
        self.menu.show()
        self.close()

    def validar_entrada(self, valor_str, nombre):
        if '/' in valor_str:
            raise ValueError(f"El valor de {nombre} contiene una fracción con '/', usa punto decimal (.) en su lugar.")
        try:
            return float(valor_str)
        except ValueError:
            raise ValueError(f"El valor de {nombre} no es un número válido.")

    def calcular(self):
        if not self.ecuacion_input.toPlainText().strip() or any(not box.text().strip() for box in self.parametros.values()):
            QMessageBox.warning(self, "Advertencia", "Por favor, complete todos los campos antes de calcular.")
            return

        try:
            f_str = self.ecuacion_input.toPlainText().replace("^", "**").replace("sen", "sin")
            f = lambdify(('x', 'y'), sympify(f_str))

            x0 = self.validar_entrada(self.parametros["x0:"].text(), "x0")
            y0 = self.validar_entrada(self.parametros["y0:"].text(), "y0")
            xf = self.validar_entrada(self.parametros["xf:"].text(), "xf")
            h = self.validar_entrada(self.parametros["h:"].text(), "h")

            x_vals = [x0]
            y_vals = [y0]
            x = x0
            y = y0

            while x <= xf:
                if self.metodo_combo.currentText() == "Euler":
                    y = y + h * f(x, y)
                elif self.metodo_combo.currentText() == "Heun":
                    k1 = f(x, y)
                    k2 = f(x + h, y + h * k1)
                    y = y + h * (k1 + k2) / 2
                elif self.metodo_combo.currentText() == "Runge-Kutta 4":
                    k1 = f(x, y)
                    k2 = f(x + h / 2, y + h * k1 / 2)
                    k3 = f(x + h / 2, y + h * k2 / 2)
                    k4 = f(x + h, y + h * k3)
                    y = y + (h / 6) * (k1 + 2 * k2 + 2 * k3 + k4)
                elif self.metodo_combo.currentText() == "Taylor":
                    x_sym, y_sym = symbols('x y')
                    f_expr = sympify(f_str)
                    df_dx = lambdify((x_sym, y_sym), diff(f_expr, x_sym))
                    df_dy = lambdify((x_sym, y_sym), diff(f_expr, y_sym))
                    y = y + h * f(x, y) + (h**2 / 2) * (df_dx(x, y) + df_dy(x, y) * f(x, y))

                x = round(x + h, 10)
                x_vals.append(x)
                y_vals.append(y)

            y_vals.append(y_vals[-1])

            self.tabla.setRowCount(len(x_vals) - 1)
            self.tabla.setColumnCount(2)
            self.tabla.setHorizontalHeaderLabels(["x", "y"])
            self.tabla.verticalHeader().setVisible(False)

            self.tabla.setColumnWidth(0, 120)
            self.tabla.setColumnWidth(1, 120)

            for i in range(len(x_vals) - 1):
                item_x = QTableWidgetItem(f"{x_vals[i]:.4f}")
                item_y = QTableWidgetItem(f"{y_vals[i + 1]:.4f}")
                item_x.setTextAlignment(Qt.AlignCenter)
                item_y.setTextAlignment(Qt.AlignCenter)
                self.tabla.setItem(i, 0, item_x)
                self.tabla.setItem(i, 1, item_y)

            self.canvas.figure.clf()
            self.canvas.figure.set_facecolor('#0f111a')
            ax = self.canvas.figure.add_subplot(111)
            ax.plot(x_vals, y_vals[1:], marker='o', color='#00d2ff')
            ax.set_title("Solución Aproximada de la EDO", color="white")
            ax.set_facecolor("#1e1e1e")
            ax.tick_params(colors="white")
            ax.spines['bottom'].set_color('white')
            ax.spines['left'].set_color('white')
            ax.yaxis.label.set_color('white')
            ax.xaxis.label.set_color('white')
            ax.grid(True, color="#444444")
            self.canvas.draw()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ha ocurrido un error: {e}")
