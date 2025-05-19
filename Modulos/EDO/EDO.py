# Se importan las herramientas necesarias para crear ventanas, botones, cuadros de texto, etc.
from PyQt5.QtWidgets import *
# Se importa una herramienta para manejar la alineación de los elementos en la ventana
from PyQt5.QtCore import Qt
# Se importa la biblioteca numpy para cálculos numéricos
import numpy as np
# Se importa matplotlib para poder graficar
import matplotlib.pyplot as plt
# Se importa una herramienta que permite mostrar gráficos de matplotlib dentro de la ventana
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# Se importa sympy, que sirve para trabajar con fórmulas matemáticas de forma simbólica
from sympy import *
# Se importan dos herramientas adicionales para mostrar mensajes y trabajar con tablas
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox

# Se importa una clase que representa el menú principal de la aplicación
from Modulos.menu_general.menu_general import MenuGeneral
# Se importa una barra de herramientas para interactuar con los gráficos (como hacer zoom o mover)
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


# Se crea una clase llamada EDO que representa la ventana para resolver ecuaciones diferenciales ordinarias
class EDO(QWidget):
    def __init__(self):
        super().__init__()  # Se inicializa la ventana
        self.setWindowTitle("Resolución de EDOs")  # Título de la ventana
        # Se establece un estilo visual con colores oscuros y texto blanco
        self.setStyleSheet("background-color: #0f111a; color: white; font-size: 16px;")
        self.setGeometry(100, 100, 1000, 600)  # Tamaño y posición inicial de la ventana

        layout = QVBoxLayout(self)  # Se crea un diseño vertical para organizar los elementos

        # Se agrega un título visual llamativo en la parte superior
        titulo = QLabel("📈 Resolución de EDOs")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 28px; font-weight: bold; color: #00d2ff;")
        layout.addWidget(titulo)

        # Se crea una caja de texto donde el usuario escribirá la ecuación diferencial
        self.ecuacion_input = QTextEdit()
        self.ecuacion_input.setPlaceholderText("Escribe la EDO como y' = x/y")
        self.ecuacion_input.setStyleSheet("background-color: #1e1e1e; border: 1px solid #00d2ff; border-radius: 10px;")
        self.ecuacion_input.setFixedHeight(80)
        layout.addWidget(self.ecuacion_input)

        # Se crean campos para que el usuario escriba los valores iniciales
        parametros_layout = QGridLayout()
        labels = ["x0:", "y0:", "xf(n):", "h:"]  # Nombres de los parámetros
        self.parametros = {}  # Diccionario para guardar las cajas de texto
        for i, label in enumerate(labels):
            lbl = QLabel(label)  # Se crea la etiqueta
            lbl.setStyleSheet("color: white;")
            parametros_layout.addWidget(lbl, 0, i)
            box = QLineEdit()  # Se crea la caja de texto
            box.setStyleSheet("background-color: #1e1e1e; border: 1px solid #00d2ff; border-radius: 8px; padding: 6px;")
            self.parametros[label] = box  # Se guarda
            parametros_layout.addWidget(box, 1, i)

        layout.addLayout(parametros_layout)

        # Se crean botones para elegir método, calcular, limpiar y salir
        fila_botones = QHBoxLayout()
        self.metodo_combo = QComboBox()
        self.metodo_combo.addItems(["Euler", "Heun", "Runge-Kutta 4", "Taylor", "Ver todas"])
        self.metodo_combo.setStyleSheet("background-color: #1e1e1e; border: 1px solid #00d2ff; color: white;")
        fila_botones.addWidget(self.metodo_combo)

        # Botón para calcular la solución
        boton_calcular = QPushButton("Calcular")
        boton_calcular.setCursor(Qt.PointingHandCursor)
        boton_calcular.setStyleSheet("background-color: #00d2ff; font-weight: bold; border-radius: 10px; padding: 10px;")
        boton_calcular.clicked.connect(self.calcular)  # Se conecta a la función calcular
        fila_botones.addWidget(boton_calcular)

        # Botón para limpiar los campos
        boton_limpiar = QPushButton("Limpiar")
        boton_limpiar.setCursor(Qt.PointingHandCursor)
        boton_limpiar.setStyleSheet("background-color: #ff6f61; font-weight: bold; border-radius: 10px; padding: 10px;")
        boton_limpiar.clicked.connect(self.limpiar_campos)
        fila_botones.addWidget(boton_limpiar)

        # Botón para salir y volver al menú
        boton_salir = QPushButton("Salir")
        boton_salir.setCursor(Qt.PointingHandCursor)
        boton_salir.setStyleSheet("background-color: #ff4757; font-weight: bold; border-radius: 10px; padding: 10px;")
        boton_salir.clicked.connect(self.volver)
        fila_botones.addWidget(boton_salir)

        layout.addLayout(fila_botones)

        # Se crean dos zonas principales: una para el gráfico y otra para la tabla
        contenido_layout = QHBoxLayout()

        # Se crea el área donde se va a mostrar la gráfica
        self.canvas = FigureCanvas(plt.figure(facecolor='#0f111a'))
        self.canvas.setFixedWidth(600)
        self.toolbar = NavigationToolbar(self.canvas, self)  # Barra de herramientas para el gráfico
        layout.addWidget(self.toolbar)
        self.toolbar.setStyleSheet("""  # Estilos visuales de la barra
            QToolBar {
                background-color: #1e1e1e;
                border: none;
            }
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

        contenido_layout.addWidget(self.canvas)

        # Se crea la tabla donde se mostrarán los valores numéricos de la solución
        self.tabla = QTableWidget()
        self.tabla.setStyleSheet("background-color: #1e1e1e; border: 1px solid #00d2ff; color: white;")
        self.tabla.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tabla.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tabla.setFixedWidth(600)
        self.tabla.setFixedHeight(310)
        self.tabla.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tabla.setSelectionMode(QAbstractItemView.NoSelection)
        contenido_layout.addWidget(self.tabla)

        layout.addLayout(contenido_layout)

    # Esta función borra todo lo que el usuario haya escrito o generado
    def limpiar_campos(self):
        self.ecuacion_input.clear()
        for box in self.parametros.values():
            box.clear()
        self.tabla.clear()
        self.canvas.figure.clear()
        self.canvas.draw()

    # Esta función cierra esta ventana y regresa al menú principal
    def volver(self):
        self.menu = MenuGeneral()
        self.menu.show()
        self.close()

    # Esta función valida que los valores escritos sean números válidos
    def validar_entrada(self, valor_str, nombre):
        if '/' in valor_str:
            raise ValueError(f"El valor de {nombre} contiene una fracción con '/', usa punto decimal (.) en su lugar.")
        try:
            return float(valor_str)
        except ValueError:
            raise ValueError(f"El valor de {nombre} no es un número válido.")

    # Esta función es la que realiza el cálculo según el método seleccionado
    def calcular(self):
        # Primero, se revisa que todos los campos estén llenos
        if not self.ecuacion_input.toPlainText().strip() or any(not box.text().strip() for box in self.parametros.values()):
            QMessageBox.warning(self, "Advertencia", "Por favor, complete todos los campos antes de calcular.")
            return

        try:
            # Se toma la ecuación escrita y se prepara para que la computadora pueda entenderla
            f_str = self.ecuacion_input.toPlainText().replace("^", "**").replace("sen", "sin")
            f = lambdify(('x', 'y'), sympify(f_str))

            # Se obtienen los valores numéricos ingresados por el usuario
            x0 = self.validar_entrada(self.parametros["x0:"].text(), "x0")
            y0 = self.validar_entrada(self.parametros["y0:"].text(), "y0")
            xf = self.validar_entrada(self.parametros["xf(n):"].text(), "xf(n)")
            h = self.validar_entrada(self.parametros["h:"].text(), "h")

            metodo_seleccionado = self.metodo_combo.currentText()

            # Si el usuario quiere ver todos los métodos, se calculan todos
            metodos = ["Euler", "Heun", "Runge-Kutta 4", "Taylor"] if metodo_seleccionado == "Ver todas" else [metodo_seleccionado]

            resultados = {}
            x_vals = np.arange(x0, xf + h, h)
            x_vals = np.round(x_vals, 10)

            # Se aplica el método seleccionado para calcular los valores de y
            for metodo in metodos:
                y = y0
                ys = [y0]
                for x in x_vals[:-1]:
                    if metodo == "Euler":
                        y = y + h * f(x, y)
                    elif metodo == "Heun":
                        k1 = f(x, y)
                        k2 = f(x + h, y + h * k1)
                        y = y + h * (k1 + k2) / 2
                    elif metodo == "Runge-Kutta 4":
                        k1 = f(x, y)
                        k2 = f(x + h / 2, y + h * k1 / 2)
                        k3 = f(x + h / 2, y + h * k2 / 2)
                        k4 = f(x + h, y + h * k3)
                        y = y + (h / 6) * (k1 + 2 * k2 + 2 * k3 + k4)
                    elif metodo == "Taylor":
                        x_sym, y_sym = symbols('x y')
                        f_expr = sympify(f_str)
                        df_dx = lambdify((x_sym, y_sym), diff(f_expr, x_sym))
                        df_dy = lambdify((x_sym, y_sym), diff(f_expr, y_sym))
                        y = y + h * f(x, y) + (h**2 / 2) * (df_dx(x, y) + df_dy(x, y) * f(x, y))
                    ys.append(y)
                resultados[metodo] = ys

            # Se muestran los resultados en una tabla
            self.tabla.setRowCount(len(x_vals))
            self.tabla.setColumnCount(len(metodos) + 1)
            self.tabla.setHorizontalHeaderLabels(["x"] + metodos)
            self.tabla.verticalHeader().setVisible(False)

            col_width = 600 // (len(metodos) + 1)
            for col in range(len(metodos) + 1):
                self.tabla.setColumnWidth(col, col_width)

            for i, x in enumerate(x_vals):
                self.tabla.setItem(i, 0, QTableWidgetItem(f"{x:.4f}"))
                self.tabla.item(i, 0).setTextAlignment(Qt.AlignCenter)
                for j, metodo in enumerate(metodos):
                    item = QTableWidgetItem(f"{resultados[metodo][i]:.4f}")
                    item.setTextAlignment(Qt.AlignCenter)
                    self.tabla.setItem(i, j + 1, item)

            # Se dibuja la gráfica con los resultados obtenidos
            self.canvas.figure.clf()
            self.canvas.figure.set_facecolor('#0f111a')
            ax = self.canvas.figure.add_subplot(111)

            colores = ['#00d2ff', '#00ff99', '#ffcc00', '#ff5050']
            for i, metodo in enumerate(metodos):
                ax.plot(x_vals, resultados[metodo], marker='o', label=metodo, color=colores[i % len(colores)])

            ax.set_title("Soluciones Aproximadas", color="white")
            ax.set_facecolor("#1e1e1e")
            ax.tick_params(colors="white")
            ax.spines['bottom'].set_color('white')
            ax.spines['left'].set_color('white')
            ax.yaxis.label.set_color('white')
            ax.xaxis.label.set_color('white')
            ax.grid(True, color="#444444")
            ax.legend(facecolor="#1e1e1e", edgecolor="white", labelcolor="white")

            self.canvas.draw()

        # Si ocurre algún error, se muestra un mensaje
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ha ocurrido un error: {e}")
