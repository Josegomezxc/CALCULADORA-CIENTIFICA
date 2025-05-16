import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from utils.helpers import resource_path
from Modulos.menu_general.menu_general import MenuGeneral
import math
import sympy as sp


class MonteCarlo(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("🎲 Método Monte Carlo")
        self.setGeometry(100, 100, 1100, 720)
        self.setStyleSheet(self.estilos())

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        # Título
        titulo = QLabel("🎲 Integración por Método Monte Carlo")
        titulo.setObjectName("titulo")
        main_layout.addWidget(titulo)

        # Formulario
        form = QGridLayout()
        form.setHorizontalSpacing(20)
        form.setVerticalSpacing(10)
        
        form.addWidget(QLabel("f1(x) ="), 0, 0, alignment=Qt.AlignRight)
        self.func1_input = QLineEdit("x^2")
        form.addWidget(self.func1_input, 0, 1)

        form.addWidget(QLabel("f2(x) ="), 0, 2, alignment=Qt.AlignRight)
        self.func2_input = QLineEdit("sqrt(x)")
        self.func2_input.setPlaceholderText("Opcional")
        form.addWidget(self.func2_input, 0, 3)

        form.addWidget(QLabel("Límite inferior (a):"), 1, 0, alignment=Qt.AlignRight)
        self.a_input = QLineEdit("0")
        form.addWidget(self.a_input, 1, 1)

        form.addWidget(QLabel("Límite superior (b):"), 1, 2, alignment=Qt.AlignRight)
        self.b_input = QLineEdit("1")
        form.addWidget(self.b_input, 1, 3)

        form.addWidget(QLabel("Número de muestras (N):"), 2, 0, alignment=Qt.AlignRight)
        self.n_input = QSpinBox()
        self.n_input.setRange(100, 1_000_000)
        self.n_input.setValue(10000)
        form.addWidget(self.n_input, 2, 1)

        main_layout.addLayout(form)

        # Botones en fila
        botones_layout = QHBoxLayout()
        botones_layout.setSpacing(15)

        self.calc_btn = QPushButton("Calcular")
        self.calc_btn.setObjectName("botonAccion")
        self.calc_btn.setCursor(Qt.PointingHandCursor)
        self.calc_btn.clicked.connect(self.calcular)
        botones_layout.addWidget(self.calc_btn)

        limpiar_btn = QPushButton("Limpiar")
        limpiar_btn.setObjectName("botonLimpiar")
        limpiar_btn.setCursor(Qt.PointingHandCursor)
        limpiar_btn.clicked.connect(self.limpiar)
        botones_layout.addWidget(limpiar_btn)

        volver_btn = QPushButton("Volver al menú principal")
        volver_btn.setObjectName("botonAccion")
        volver_btn.setCursor(Qt.PointingHandCursor)
        volver_btn.clicked.connect(self.volver)
        botones_layout.addWidget(volver_btn)

        main_layout.addLayout(botones_layout)

        # Sección gráfica y resultados
        content_layout = QHBoxLayout()
        content_layout.setSpacing(20)

        # Tabla de resultados
        self.tabla = QTableWidget(5, 1)
        self.tabla.setHorizontalHeaderLabels(["Valor"])
        self.tabla.setVerticalHeaderLabels([
            "Integral exacta", "Aproximación MC","Área estimada",
            "Puntos dentro", "Puntos fuera"
        ])
        self.tabla.horizontalHeader().setStretchLastSection(True)
        self.tabla.setStyleSheet("color: white; background-color: #1e1e1e; border: 1px solid #00d2ff;")
        content_layout.addWidget(self.tabla, stretch=1)

        # Gráfica
        self.figure = plt.Figure(figsize=(6, 5), dpi=100, facecolor=(0, 0, 0, 0))
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setStyleSheet("background: transparent;")
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.toolbar.setStyleSheet("""
            QToolBar { background-color: #1e1e1e; border: none; }
            QToolButton {
                background-color: #2b2b2b;
                border: 1px solid #00d2ff;
                border-radius: 4px;
                padding: 4px;
                color: white;
            }
            QToolButton:hover {
                background-color: #00d2ff;
                color: black;
            }
        """)
        graph_layout = QVBoxLayout()
        graph_layout.addWidget(self.toolbar)
        graph_layout.addWidget(self.canvas)
        content_layout.addLayout(graph_layout, stretch=2)

        main_layout.addLayout(content_layout)

    def limpiar(self):
        self.func1_input.clear()
        self.func2_input.clear()
        self.a_input.setText("0")
        self.b_input.setText("3.1416")
        self.n_input.setValue(10000)
        self.tabla.clearContents()
        self.figure.clear()
        self.canvas.draw()

    def calcular(self):
        try:
            a = float(self.a_input.text())
            b = float(self.b_input.text())
            n = int(self.n_input.value())

            fx1_str = self.func1_input.text().replace("^", "**").strip()
            fx2_str = self.func2_input.text().replace("^", "**").strip()

            # Definir el scope para eval
            scope = {"x": None, "sin": np.sin, "cos": np.cos, "exp": np.exp,
                    "log": np.log, "sqrt": np.sqrt, "abs": np.abs, "tan": np.tan}

            x_vals = np.random.uniform(a, b, n)

            # Condicional según funciones ingresadas
            if fx1_str and not fx2_str:
                # Solo f1
                scope["x"] = x_vals
                fx1 = eval(fx1_str, scope)
                y_vals = np.random.uniform(fx1.min(), fx1.max(), n)
                puntos_dentro_mask = (y_vals <= fx1)
                puntos_fuera_mask = ~puntos_dentro_mask
                area_estim = (b - a) * (fx1.max() - fx1.min()) * (np.sum(puntos_dentro_mask) / n)

                # Integral y estimaciones
                x = sp.Symbol("x")
                try:
                    expr1 = sp.sympify(fx1_str)
                    integral = sp.integrate(expr1, (x, a, b)).evalf()
                except:
                    integral = "No disponible"

                self.tabla.setItem(0, 0, QTableWidgetItem(str(integral)))
                self.tabla.setItem(1, 0, QTableWidgetItem(f"{np.mean(fx1) * (b - a):.6f}"))
                self.tabla.setItem(2, 0, QTableWidgetItem(f"{area_estim:.6f}"))
                self.tabla.setItem(3, 0, QTableWidgetItem(str(np.sum(puntos_dentro_mask))))
                self.tabla.setItem(4, 0, QTableWidgetItem(str(np.sum(puntos_fuera_mask))))

                ys1 = eval(fx1_str, {**scope, "x": np.linspace(a, b, 300)})
                ys2 = None

            elif fx2_str and not fx1_str:
                # Solo f2
                scope["x"] = x_vals
                fx2 = eval(fx2_str, scope)
                y_vals = np.random.uniform(fx2.min(), fx2.max(), n)
                puntos_dentro_mask = (y_vals <= fx2)
                puntos_fuera_mask = ~puntos_dentro_mask
                area_estim = (b - a) * (fx2.max() - fx2.min()) * (np.sum(puntos_dentro_mask) / n)

                # Integral y estimaciones
                x = sp.Symbol("x")
                try:
                    expr2 = sp.sympify(fx2_str)
                    integral = sp.integrate(expr2, (x, a, b)).evalf()
                except:
                    integral = "No disponible"

                self.tabla.setItem(0, 0, QTableWidgetItem(str(integral)))
                self.tabla.setItem(1, 0, QTableWidgetItem(f"{np.mean(fx2) * (b - a):.6f}"))
                self.tabla.setItem(2, 0, QTableWidgetItem(f"{area_estim:.6f}"))
                self.tabla.setItem(3, 0, QTableWidgetItem(str(np.sum(puntos_dentro_mask))))
                self.tabla.setItem(4, 0, QTableWidgetItem(str(np.sum(puntos_fuera_mask))))

                ys1 = None
                ys2 = eval(fx2_str, {**scope, "x": np.linspace(a, b, 300)})

            elif fx1_str and fx2_str:
                # Ambas funciones
                scope["x"] = x_vals
                fx1 = eval(fx1_str, scope)
                fx2 = eval(fx2_str, scope)
                y_vals = np.random.uniform(min(fx1.min(), fx2.min()), max(fx1.max(), fx2.max()), n)

                y_min = np.minimum(fx1, fx2)
                y_max = np.maximum(fx1, fx2)

                puntos_dentro_mask = (y_vals >= y_min) & (y_vals <= y_max)
                puntos_fuera_mask = ~puntos_dentro_mask

                puntos_dentro = np.sum(puntos_dentro_mask)
                puntos_fuera = n - puntos_dentro
                area_estim = (b - a) * (y_max.max() - y_min.min()) * (puntos_dentro / n)

                x = sp.Symbol("x")
                try:
                    expr1 = sp.sympify(fx1_str)
                    expr2 = sp.sympify(fx2_str)
                    integral = sp.integrate(expr1 - expr2, (x, a, b)).evalf()
                except:
                    integral = "No disponible"

                self.tabla.setItem(0, 0, QTableWidgetItem(str(integral)))
                self.tabla.setItem(1, 0, QTableWidgetItem(f"{np.mean(fx1 - fx2) * (b - a):.6f}"))
                self.tabla.setItem(2, 0, QTableWidgetItem(f"{area_estim:.6f}"))
                self.tabla.setItem(3, 0, QTableWidgetItem(str(puntos_dentro)))
                self.tabla.setItem(4, 0, QTableWidgetItem(str(puntos_fuera)))

                xs = np.linspace(a, b, 300)
                ys1 = eval(fx1_str, {**scope, "x": xs})
                ys2 = eval(fx2_str, {**scope, "x": xs})

            else:
                QMessageBox.warning(self, "Entrada vacía", "Por favor, ingrese al menos una función válida.")
                return

            # Gráfica
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            self.figure.patch.set_alpha(0)
            ax.set_facecolor((0, 0, 0, 0))
            ax.tick_params(colors='white')
            ax.xaxis.label.set_color('white')
            ax.yaxis.label.set_color('white')

            xs = np.linspace(a, b, 300)

            if ys1 is not None:
                ax.plot(xs, ys1, label="f1(x)", color="#502180")
            if ys2 is not None:
                ax.plot(xs, ys2, label="f2(x)", color="#1C781C")

            # Si hay puntos dentro y fuera definidos
            if 'puntos_dentro_mask' in locals() and 'puntos_fuera_mask' in locals():
                x_dentro = x_vals[puntos_dentro_mask]
                y_dentro = y_vals[puntos_dentro_mask]
                x_fuera = x_vals[puntos_fuera_mask]
                y_fuera = y_vals[puntos_fuera_mask]

                ax.scatter(x_dentro[:3000], y_dentro[:3000], s=3, alpha=0.6, color="#0077ff", label="Puntos dentro")
                ax.scatter(x_fuera[:3000], y_fuera[:3000], s=3, alpha=0.3, color="#ff6600", label="Puntos fuera")

            # Solo si hay ambas funciones para rellenar el área entre ellas
            if ys1 is not None and ys2 is not None:
                ax.fill_between(xs, ys1, ys2, where=(ys1 > ys2), color="#1C781C", alpha=0.2)
                ax.fill_between(xs, ys1, ys2, where=(ys1 <= ys2), color="#502180", alpha=0.2)

            ax.set_title("Monte Carlo: Área entre curvas", color="#FFFFFF")
            ax.legend()
            ax.grid(True, alpha=0.3)
            self.canvas.draw()

        except Exception as e:
            QMessageBox.critical(self, "Error de función", f"❌ Error evaluando las funciones.\n\nDetalles: {e}")

    def volver(self):
        self.menu = MenuGeneral()
        self.menu.show()
        self.close()

    @staticmethod
    def estilos():
        return """
        QWidget {
            background-color: #0f111a;
            color: #f1f1f1;
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 15px;
        }
        QLabel#titulo {
            font-size: 28px;
            font-weight: bold;
            padding: 18px;
            background-color: #1a1d2e;
            border-bottom: 3px solid #00d2ff;
            color: #00d2ff;
            qproperty-alignment: AlignCenter;
        }
        QPushButton#botonAccion {
            background-color: qlineargradient(
                x1:0, y1:0, x2:1, y2:1,
                stop:0 #00d2ff,
                stop:1 #3a7bd5
            );
            border: none;
            border-radius: 12px;
            padding: 12px;
            font-size: 16px;
            font-weight: bold;
            color: white;
        }
        QPushButton#botonAccion:hover {
            background-color: qlineargradient(
                x1:0, y1:0, x2:1, y2:1,
                stop:0 #3a7bd5,
                stop:1 #00d2ff
            );
            border: 2px solid #00d2ff;
        }
        QPushButton#botonLimpiar {
            background-color: #aa1e1e;
            border: none;
            border-radius: 12px;
            padding: 12px;
            font-size: 16px;
            font-weight: bold;
            color: white;
        }
        QPushButton#botonLimpiar:hover {
            background-color: #ff3333;
        }
        """
