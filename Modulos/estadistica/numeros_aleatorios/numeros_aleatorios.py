import sys
import random
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QComboBox, QSpinBox, QTableView, QGridLayout, QAbstractItemView, QLineEdit, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QDoubleValidator
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from scipy.stats import norm, expon, binom, uniform, poisson, geom, gaussian_kde

# Métodos de generación de números aleatorios
def mersenne_twister(cantidad):
    return [random.random() for _ in range(cantidad)]

def xorshift32(seed, cantidad):
    resultados = []
    x = seed
    for _ in range(cantidad):
        x ^= (x << 13) & 0xFFFFFFFF
        x ^= (x >> 17)
        x ^= (x << 5) & 0xFFFFFFFF
        resultados.append((x & 0xFFFFFFFF) / 0xFFFFFFFF)
    return resultados

def pcg32(seed, cantidad):
    state = seed
    resultados = []
    for _ in range(cantidad):
        state = (state * 6364136223846793005 + 1) & 0xFFFFFFFFFFFFFFFF
        xorshifted = (((state >> 18) ^ state) >> 27) & 0xFFFFFFFF
        rot = (state >> 59) & 0x1F
        result = ((xorshifted >> rot) | (xorshifted << ((-rot) & 31))) & 0xFFFFFFFF
        resultados.append(result / 0xFFFFFFFF)
    return resultados

def well512(state, cantidad):
    results = []
    index = 0
    for _ in range(cantidad):
        a = state[index]
        c = state[(index + 13) & 15]
        b = a ^ c ^ (a << 16) ^ (c << 15)
        c = state[(index + 9) & 15]
        c ^= (c >> 11)
        a = b ^ c
        state[index] = a
        index = (index + 15) & 15
        results.append((a & 0xFFFFFFFF) / 0xFFFFFFFF)
    return results

def congruencial_lineal(x0, a, c, m, cantidad):
    resultados = []
    x = x0
    for _ in range(cantidad):
        x = (a * x + c) % m
        resultados.append(x / (m - 1))
    return resultados

def congruencial_multiplicativo(x0, a, m, cantidad):
    resultados = []
    x = x0
    for _ in range(cantidad):
        x = (a * x) % m
        resultados.append(x / (m - 1))
    return resultados

def tausworthe(seed, cantidad, q=5, r=17, s=31):
    resultados = []
    x = seed
    for _ in range(cantidad):
        b = ((x << q) ^ x) >> r
        x = ((x & ((1 << s) - 1)) << r) ^ b
        resultados.append((x & 0xFFFFFFFF) / 0xFFFFFFFF)
    return resultados

def lfsr(seed, taps, cantidad, bits=16):
    resultados = []
    sr = seed
    for _ in range(cantidad):
        bit = 0
        for t in taps:
            bit ^= (sr >> t) & 1
        sr = ((sr << 1) | bit) & ((1 << bits) - 1)
        resultados.append(sr / ((1 << bits) - 1))
    return resultados

def cuadrados_medios(semilla, cantidad, digitos):
    resultados = []
    x = semilla
    for _ in range(cantidad):
        x_cuadrado = str(x ** 2).zfill(2 * digitos)
        mitad = len(x_cuadrado) // 2
        inicio = mitad - digitos // 2
        x = int(x_cuadrado[inicio:inicio + digitos])
        resultados.append(x / (10 ** digitos))
    return resultados

def producto_medio(x0, x1, cantidad, digitos):
    resultados = []
    for _ in range(cantidad):
        prod = str(x0 * x1).zfill(2 * digitos)
        mitad = len(prod) // 2
        inicio = mitad - digitos // 2
        x2 = int(prod[inicio:inicio + digitos])
        resultados.append(x2 / (10 ** digitos))
        x0, x1 = x1, x2
    return resultados

# Interfaz Gráfica
class NumerosAleatorios(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🔢 Generador de Números Pseudoaleatorios")
        self.setGeometry(100, 100, 1000, 600)
        self.setStyleSheet("background-color: #0f111a; color: white; font-size: 16px;")

        layout = QHBoxLayout(self)

        # Panel de configuración
        left_layout = QVBoxLayout()

        # Título
        titulo = QLabel("🎲 Generación de Números Aleatorios")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 24px; font-weight: bold; color: #00d2ff;")
        left_layout.addWidget(titulo)

        # Parámetros
        self.form_layout = QGridLayout()

        self.combo = QComboBox()
        self.combo.addItems([
            "Mersenne Twister", "XORShift", "PCG", "WELL512", "Congruencial Lineal",
            "Congruencial Multiplicativo", "Tausworthe", "LFSR", "Cuadrados Medios", "Producto Medio"
        ])
        self.combo.setStyleSheet("background-color: #1e1e1e; border: 1px solid #00d2ff; border-radius: 6px; padding: 4px;")
        self.form_layout.addWidget(QLabel("Método:"), 0, 0)
        self.form_layout.addWidget(self.combo, 0, 1)

        self.distribucion_combo = QComboBox()
        self.distribucion_combo.addItems([
            "Normal", "Exponencial", "Binomial", "Uniforme", "Poisson", "Geométrica"
        ])
        self.distribucion_combo.setStyleSheet("background-color: #1e1e1e; border: 1px solid #00d2ff; border-radius: 6px; padding: 4px;")
        self.distribucion_combo.currentIndexChanged.connect(self.actualizar_parametros_distribucion)
        self.form_layout.addWidget(QLabel("Distribución:"), 1, 0)
        self.form_layout.addWidget(self.distribucion_combo, 1, 1)

        self.cantidad = QSpinBox()
        self.cantidad.setRange(1, 10000)
        self.cantidad.setValue(100)
        self.cantidad.setStyleSheet("background-color: #1e1e1e; border: 1px solid #00d2ff; border-radius: 6px; padding: 4px;")
        self.form_layout.addWidget(QLabel("Cantidad a generar:"), 2, 0)
        self.form_layout.addWidget(self.cantidad, 2, 1)

        self.semilla = QSpinBox()
        self.semilla.setRange(0, 999999)
        self.semilla.setValue(12345)
        self.semilla.setStyleSheet("background-color: #1e1e1e; border: 1px solid #00d2ff; border-radius: 6px; padding: 4px;")
        self.form_layout.addWidget(QLabel("Semilla (si aplica):"), 3, 0)
        self.form_layout.addWidget(self.semilla, 3, 1)

        # Contenedor para parámetros de distribución
        self.param_layout = QVBoxLayout()
        self.form_layout.addLayout(self.param_layout, 4, 0, 1, 2)

        left_layout.addLayout(self.form_layout)

        # Botones en una fila
        button_layout = QHBoxLayout()

        btn_generar = QPushButton("Generar")
        btn_generar.setCursor(Qt.PointingHandCursor)
        btn_generar.setStyleSheet("background-color: #00d2ff; font-weight: bold; border-radius: 10px; padding: 10px;")
        btn_generar.clicked.connect(self.generar)
        button_layout.addWidget(btn_generar)

        btn_limpiar = QPushButton("Limpiar")
        btn_limpiar.setCursor(Qt.PointingHandCursor)
        btn_limpiar.setStyleSheet("background-color: #ff5733; font-weight: bold; border-radius: 10px; padding: 10px;")
        btn_limpiar.clicked.connect(self.limpiar)
        button_layout.addWidget(btn_limpiar)

        btn_volver = QPushButton("Volver")
        btn_volver.setCursor(Qt.PointingHandCursor)
        btn_volver.setStyleSheet("background-color: #00d2ff; font-weight: bold; border-radius: 10px; padding: 10px;")
        btn_volver.clicked.connect(self.volver)
        button_layout.addWidget(btn_volver)

        left_layout.addLayout(button_layout)

        # Canvas para gráfica
        self.canvas = FigureCanvas(plt.figure(facecolor='#0f111a'))
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
        left_layout.addWidget(self.toolbar)
        left_layout.addWidget(self.canvas)

        # Panel de tabla
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['Índice', 'Valor generado'])

        self.table = QTableView()
        self.table.setModel(self.model)
        self.table.setStyleSheet("background-color: #1e1e1e; color: white; border: 1px solid #00d2ff;")
        self.table.horizontalHeader().setStyleSheet("QHeaderView::section { background-color: #1e1e1e; color: #00d2ff; }")
        self.table.setMaximumWidth(320)  # Limita el ancho total de la tabla
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        layout.addLayout(left_layout)
        layout.addWidget(self.table)

        # Inicializar parámetros de distribución y contador de semilla
        self.param_inputs = {}
        self.seed_counter = 0
        self.actualizar_parametros_distribucion()

    def actualizar_parametros_distribucion(self):
        # Limpiar el layout de parámetros
        for i in reversed(range(self.param_layout.count())):
            widget = self.param_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)
            else:
                layout = self.param_layout.itemAt(i).layout()
                if layout is not None:
                    for j in reversed(range(layout.count())):
                        widget = layout.itemAt(j).widget()
                        if widget is not None:
                            widget.setParent(None)
                    layout.setParent(None)
        self.param_inputs = {}

        distribucion = self.distribucion_combo.currentText()
        validator = QDoubleValidator()
        validator.setNotation(QDoubleValidator.StandardNotation)

        if distribucion == "Normal":
            mu_layout = QHBoxLayout()
            mu_layout.addWidget(QLabel("Media (μ):"))
            self.param_inputs['mu'] = QLineEdit("0")
            self.param_inputs['mu'].setValidator(validator)
            self.param_inputs['mu'].setStyleSheet("background-color: #1e1e1e; border: 1px solid #00d2ff; border-radius: 6px; padding: 4px;")
            mu_layout.addWidget(self.param_inputs['mu'])
            self.param_layout.addLayout(mu_layout)

            sigma_layout = QHBoxLayout()
            sigma_layout.addWidget(QLabel("Desviación estándar (σ):"))
            self.param_inputs['sigma'] = QLineEdit("1")
            self.param_inputs['sigma'].setValidator(validator)
            self.param_inputs['sigma'].setStyleSheet("background-color: #1e1e1e; border: 1px solid #00d2ff; border-radius: 6px; padding: 4px;")
            sigma_layout.addWidget(self.param_inputs['sigma'])
            self.param_layout.addLayout(sigma_layout)

        elif distribucion == "Exponencial":
            lambda_layout = QHBoxLayout()
            lambda_layout.addWidget(QLabel("Tasa (λ):"))
            self.param_inputs['lambda'] = QLineEdit("1")
            self.param_inputs['lambda'].setValidator(validator)
            self.param_inputs['lambda'].setStyleSheet("background-color: #1e1e1e; border: 1px solid #00d2ff; border-radius: 6px; padding: 4px;")
            lambda_layout.addWidget(self.param_inputs['lambda'])
            self.param_layout.addLayout(lambda_layout)

        elif distribucion == "Binomial":
            n_layout = QHBoxLayout()
            n_layout.addWidget(QLabel("Número de ensayos (n):"))
            self.param_inputs['n'] = QLineEdit("10")
            self.param_inputs['n'].setValidator(QDoubleValidator(bottom=1))
            self.param_inputs['n'].setStyleSheet("background-color: #1e1e1e; border: 1px solid #00d2ff; border-radius: 6px; padding: 4px;")
            n_layout.addWidget(self.param_inputs['n'])
            self.param_layout.addLayout(n_layout)

            p_layout = QHBoxLayout()
            p_layout.addWidget(QLabel("Probabilidad (p):"))
            self.param_inputs['p'] = QLineEdit("0.5")
            self.param_inputs['p'].setValidator(QDoubleValidator(bottom=0, top=1))
            self.param_inputs['p'].setStyleSheet("background-color: #1e1e1e; border: 1px solid #00d2ff; border-radius: 6px; padding: 4px;")
            p_layout.addWidget(self.param_inputs['p'])
            self.param_layout.addLayout(p_layout)

        elif distribucion == "Uniforme":
            a_layout = QHBoxLayout()
            a_layout.addWidget(QLabel("Límite inferior (a):"))
            self.param_inputs['a'] = QLineEdit("0")
            self.param_inputs['a'].setValidator(validator)
            self.param_inputs['a'].setStyleSheet("background-color: #1e1e1e; border: 1px solid #00d2ff; border-radius: 6px; padding: 4px;")
            a_layout.addWidget(self.param_inputs['a'])
            self.param_layout.addLayout(a_layout)

            b_layout = QHBoxLayout()
            b_layout.addWidget(QLabel("Límite superior (b):"))
            self.param_inputs['b'] = QLineEdit("1")
            self.param_inputs['b'].setValidator(validator)
            self.param_inputs['b'].setStyleSheet("background-color: #1e1e1e; border: 1px solid #00d2ff; border-radius: 6px; padding: 4px;")
            b_layout.addWidget(self.param_inputs['b'])
            self.param_layout.addLayout(b_layout)

        elif distribucion == "Poisson":
            lambda_layout = QHBoxLayout()
            lambda_layout.addWidget(QLabel("Tasa (λ):"))
            self.param_inputs['lambda'] = QLineEdit("1")
            self.param_inputs['lambda'].setValidator(validator)
            self.param_inputs['lambda'].setStyleSheet("background-color: #1e1e1e; border: 1px solid #00d2ff; border-radius: 6px; padding: 4px;")
            lambda_layout.addWidget(self.param_inputs['lambda'])
            self.param_layout.addLayout(lambda_layout)

        elif distribucion == "Geométrica":
            p_layout = QHBoxLayout()
            p_layout.addWidget(QLabel("Probabilidad (p):"))
            self.param_inputs['p'] = QLineEdit("0.5")
            self.param_inputs['p'].setValidator(QDoubleValidator(bottom=0, top=1))
            self.param_inputs['p'].setStyleSheet("background-color: #1e1e1e; border: 1px solid #00d2ff; border-radius: 6px; padding: 4px;")
            p_layout.addWidget(self.param_inputs['p'])
            self.param_layout.addLayout(p_layout)

    def generar(self):
        metodo = self.combo.currentText()
        distribucion = self.distribucion_combo.currentText()
        n = self.cantidad.value()
        seed = self.semilla.value() + self.seed_counter
        resultados_base = []

        # Generar números pseudoaleatorios base con semilla dinámica
        random.seed(seed)
        np.random.seed(seed)
        if metodo == "Mersenne Twister":
            resultados_base = mersenne_twister(n)
        elif metodo == "XORShift":
            resultados_base = xorshift32(seed, n)
        elif metodo == "PCG":
            resultados_base = pcg32(seed, n)
        elif metodo == "WELL512":
            state = [random.getrandbits(32) for _ in range(16)]
            resultados_base = well512(state, n)
        elif metodo == "Congruencial Lineal":
            resultados_base = congruencial_lineal(seed, 1664525, 1013904223, 2**32, n)
        elif metodo == "Congruencial Multiplicativo":
            resultados_base = congruencial_multiplicativo(seed, 1664525, 2**32, n)
        elif metodo == "Tausworthe":
            resultados_base = tausworthe(seed, n)
        elif metodo == "LFSR":
            resultados_base = lfsr(seed, [0, 2, 3, 5], n)
        elif metodo == "Cuadrados Medios":
            resultados_base = cuadrados_medios(seed, n, digitos=5)
        elif metodo == "Producto Medio":
            x1 = random.randint(1000, 9999)
            x2 = random.randint(1000, 9999)
            resultados_base = producto_medio(x1, x2, n, digitos=5)

        # Transformar según la distribución
        try:
            if distribucion == "Normal":
                mu = float(self.param_inputs['mu'].text())
                sigma = float(self.param_inputs['sigma'].text())
                if sigma <= 0:
                    raise ValueError("La desviación estándar debe ser positiva.")
                resultados = norm.ppf(resultados_base, loc=mu, scale=sigma)

            elif distribucion == "Exponencial":
                lambda_rate = float(self.param_inputs['lambda'].text())
                if lambda_rate <= 0:
                    raise ValueError("La tasa λ debe ser positiva.")
                scale = 1 / lambda_rate
                resultados = expon.ppf(resultados_base, scale=scale)

            elif distribucion == "Binomial":
                n_trials = int(float(self.param_inputs['n'].text()))
                p = float(self.param_inputs['p'].text())
                if n_trials < 1:
                    raise ValueError("El número de ensayos debe ser al menos 1.")
                if not 0 <= p <= 1:
                    raise ValueError("La probabilidad p debe estar entre 0 y 1.")
                resultados = binom.ppf(resultados_base, n=n_trials, p=p)

            elif distribucion == "Uniforme":
                a = float(self.param_inputs['a'].text())
                b = float(self.param_inputs['b'].text())
                if a >= b:
                    raise ValueError("El límite inferior a debe ser menor que el límite superior b.")
                resultados = uniform.ppf(resultados_base, loc=a, scale=b-a)

            elif distribucion == "Poisson":
                lambda_rate = float(self.param_inputs['lambda'].text())
                if lambda_rate <= 0:
                    raise ValueError("La tasa λ debe ser positiva.")
                resultados = poisson.ppf(resultados_base, mu=lambda_rate)

            elif distribucion == "Geométrica":
                p = float(self.param_inputs['p'].text())
                if not 0 < p <= 1:
                    raise ValueError("La probabilidad p debe estar entre 0 y 1.")
                resultados = geom.ppf(resultados_base, p=p)

            self.mostrar_resultados(resultados, distribucion)
            self.dibujar_grafica(resultados, distribucion)

            # Incrementar el contador de semilla
            self.seed_counter += 1

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error en los parámetros de la distribución: {str(e)}")

    def mostrar_resultados(self, resultados, distribucion):
        self.model.removeRows(0, self.model.rowCount())
        for i, valor in enumerate(resultados):
            item1 = QStandardItem(str(i))
            item2 = QStandardItem(f"{valor:.6f}" if distribucion in ["Normal", "Exponencial", "Uniforme"] else str(int(valor)))
            item1.setTextAlignment(Qt.AlignCenter)
            item2.setTextAlignment(Qt.AlignCenter)
            self.model.appendRow([item1, item2])
        self.table.setColumnWidth(0, 60)
        self.table.setColumnWidth(1, 140)

    def dibujar_grafica(self, resultados, distribucion):
        plt.clf()
        fig = self.canvas.figure
        ax = fig.add_subplot(111)
        
        # Usar histograma para distribuciones continuas o barras para discretas
        if distribucion in ["Normal", "Exponencial", "Uniforme"]:
            # Histograma
            ax.hist(resultados, bins=30, density=True, alpha=0.5, color='cyan', label=f"Histograma {distribucion}")
            # Curva de densidad kernel
            kde = gaussian_kde(resultados)
            x_range = np.linspace(min(resultados), max(resultados), 200)
            ax.plot(x_range, kde(x_range), 'y-', label=f"Curva {distribucion}", linewidth=2)
        else:
            # Barras
            unique, counts = np.unique(resultados, return_counts=True)
            ax.bar(unique, counts/np.sum(counts), color='cyan', alpha=0.5, label=f"Barras {distribucion}")
            # Curva conectando las frecuencias
            ax.plot(unique, counts/np.sum(counts), 'y-', marker='o', label=f"Curva {distribucion}", linewidth=2)

        ax.set_facecolor('#0f111a')
        ax.set_xlabel('Valor', color='white')
        ax.set_ylabel('Densidad/Frecuencia', color='white')
        ax.set_title(f"Distribución {distribucion}", color='white')
        ax.legend()
        ax.grid(True, color='gray')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        self.canvas.draw()

    def limpiar(self):
        self.model.removeRows(0, self.model.rowCount())
        plt.clf()
        self.canvas.draw()
        for key in self.param_inputs:
            self.param_inputs[key].clear()
        self.seed_counter = 0  # Reiniciar el contador de semilla

    def volver(self):
        from Modulos.estadistica.estadistica import MenuEstadistica 
        self.menu = MenuEstadistica()
        self.menu.show()
        self.close()


