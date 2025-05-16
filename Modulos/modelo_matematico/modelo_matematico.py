import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


class SimuladorSIR(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📊 Simulador SIR - Modelo Epidemiológico")
        self.setGeometry(100, 100, 1000, 600)
        self.setStyleSheet("background-color: #0f111a; color: white; font-size: 16px;")

        layout = QVBoxLayout(self)

        # Título
        titulo = QLabel("📊 Simulador SIR - Modelo de Propagación Epidémica")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 28px; font-weight: bold; color: #00d2ff;")
        layout.addWidget(titulo)

        # Parámetros
        form_layout = QGridLayout()
        etiquetas = ["Población (N):", "Infectados iniciales (I₀):", "β (tasa de infección):",
                     "γ (tasa de recuperación):", "Días:"]
        self.campos = {}
        valores_defecto = ["1000", "1", "0.3", "0.1", "60"]
        for i, (etq, val) in enumerate(zip(etiquetas, valores_defecto)):
            label = QLabel(etq)
            label.setStyleSheet("color: white;")
            form_layout.addWidget(label, 0, i)
            box = QLineEdit(val)
            box.setStyleSheet("background-color: #1e1e1e; border: 1px solid #00d2ff; border-radius: 8px; padding: 6px;")
            self.campos[etq] = box
            form_layout.addWidget(box, 1, i)

        layout.addLayout(form_layout)

        # Opciones de visualización mejoradas
        group_opciones = QGroupBox("Seleccionar curvas a mostrar")
        group_opciones.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 16px;
                color: #00d2ff;
                border: 1px solid #00d2ff;
                border-radius: 10px;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)

        opciones_layout = QHBoxLayout()
        self.chk_s = QCheckBox("Susceptibles")
        self.chk_i = QCheckBox("Infectados")
        self.chk_r = QCheckBox("Recuperados")

        for chk, color in zip((self.chk_s, self.chk_i, self.chk_r), ("#00d2ff", "#ff5050", "#00ff99")):
            chk.setChecked(True)
            chk.setStyleSheet(f"""
                QCheckBox {{
                    spacing: 10px;
                    color: {color};
                    font-size: 15px;
                }}
                QCheckBox::indicator {{
                    width: 18px;
                    height: 18px;
                }}
                QCheckBox::indicator:checked {{
                    background-color: {color};
                    border: 1px solid white;
                }}
            """)
            opciones_layout.addWidget(chk)

        group_opciones.setLayout(opciones_layout)
        layout.addWidget(group_opciones)

        # Botones
        botones_layout = QHBoxLayout()

        boton_simular = QPushButton("Calcular")
        boton_simular.setCursor(Qt.PointingHandCursor)
        boton_simular.setStyleSheet("background-color: #00d2ff; font-weight: bold; border-radius: 10px; padding: 10px;")
        boton_simular.clicked.connect(self.simular)
        botones_layout.addWidget(boton_simular)

        boton_limpiar = QPushButton("Limpiar")
        boton_limpiar.setCursor(Qt.PointingHandCursor)
        boton_limpiar.setStyleSheet("background-color: #ff6f61; font-weight: bold; border-radius: 10px; padding: 10px;")
        boton_limpiar.clicked.connect(self.limpiar)
        botones_layout.addWidget(boton_limpiar)

        boton_salir = QPushButton("Salir")
        boton_salir.setCursor(Qt.PointingHandCursor)
        boton_salir.setStyleSheet("background-color: #ff4757; font-weight: bold; border-radius: 10px; padding: 10px;")
        boton_salir.clicked.connect(self.volver)
        botones_layout.addWidget(boton_salir)

        layout.addLayout(botones_layout)

        # Gráfica
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
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)

    def simular(self):
        try:
            N = int(self.campos["Población (N):"].text())
            I0 = int(self.campos["Infectados iniciales (I₀):"].text())
            R0 = 0
            S0 = N - I0
            beta = float(self.campos["β (tasa de infección):"].text())
            gamma = float(self.campos["γ (tasa de recuperación):"].text())
            dias = int(self.campos["Días:"].text())
        except ValueError:
            QMessageBox.critical(self, "Error", "Todos los campos deben contener valores numéricos válidos.")
            return

        t = np.linspace(0, dias, dias + 1)

        def deriv(y, t, N, beta, gamma):
            S, I, R = y
            dSdt = -beta * S * I / N
            dIdt = beta * S * I / N - gamma * I
            dRdt = gamma * I
            return dSdt, dIdt, dRdt

        y0 = S0, I0, R0
        sol = odeint(deriv, y0, t, args=(N, beta, gamma))
        S, I, R = sol.T

        self.canvas.figure.clf()
        self.canvas.figure.set_facecolor('#0f111a')
        ax = self.canvas.figure.add_subplot(111)

        if self.chk_s.isChecked():
            ax.plot(t, S, '-', color="#00d2ff", label="Susceptibles", linewidth=2)
        if self.chk_i.isChecked():
            ax.plot(t, I, '-', color="#ff5050", label="Infectados", linewidth=2)
        if self.chk_r.isChecked():
            ax.plot(t, R, '-', color="#00ff99", label="Recuperados", linewidth=2)

        ax.set_title("Simulación del Modelo SIR", color='white')
        ax.set_xlabel("Días", color='white')
        ax.set_ylabel("Número de Personas", color='white')
        ax.tick_params(colors='white')
        ax.set_facecolor("#1e1e1e")
        ax.grid(True, color="#444444")
        ax.legend(facecolor="#1e1e1e", edgecolor="white", labelcolor="white")
        ax.spines['bottom'].set_color('white')
        ax.spines['left'].set_color('white')

        self.canvas.draw()

    def volver(self):
        from Modulos.menu_general.menu_general import MenuGeneral
        self.menu = MenuGeneral()
        self.menu.show()
        self.close()

    def limpiar(self):
        for campo in self.campos.values():
            campo.clear()
        self.canvas.figure.clf()
        self.canvas.draw()