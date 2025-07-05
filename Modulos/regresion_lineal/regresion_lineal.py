import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QGridLayout, QTextEdit
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np

class RegresionLineal(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Regresión Lineal")
        self.setStyleSheet("background-color: #0F101A; color: white;")
        self.setGeometry(100, 100, 1200, 700)
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout()

        # Panel Izquierdo
        self.left_panel = QVBoxLayout()

        title = QLabel("📊 REGRESIÓN LINEAL")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: cyan;")
        self.left_panel.addWidget(title)

        subtitle = QLabel("Ingrese datos (una fila por par x;y: ej: 2,65 en la primera fila)")
        subtitle.setStyleSheet("font-size: 10pt; color: #00BFFF;")
        self.left_panel.addWidget(subtitle)

        self.input_grid = QGridLayout()
        self.x_inputs = []
        self.y_inputs = []

        for i in range(8):
            x_input = QLineEdit()
            y_input = QLineEdit()
            x_label = QLabel(f"X{i+1}:")
            y_label = QLabel(f"Y{i+1}:")
            x_input.setFixedWidth(60)
            y_input.setFixedWidth(60)
            self.x_inputs.append(x_input)
            self.y_inputs.append(y_input)
            self.input_grid.addWidget(x_label, i, 0)
            self.input_grid.addWidget(x_input, i, 1)
            self.input_grid.addWidget(y_label, i, 2)
            self.input_grid.addWidget(y_input, i, 3)

        self.left_panel.addLayout(self.input_grid)

        self.pred_label = QLabel("Valor de X para predicción:")
        self.left_panel.addWidget(self.pred_label)

        self.x_pred_input = QLineEdit()
        self.left_panel.addWidget(self.x_pred_input)

        self.resultado_label = QLabel("Resultado:")
        self.left_panel.addWidget(self.resultado_label)

        self.resultado_text = QTextEdit()
        self.resultado_text.setReadOnly(True)
        self.resultado_text.setFixedHeight(80)
        self.left_panel.addWidget(self.resultado_text)

        self.plot_widget = FigureCanvas(plt.Figure(figsize=(5, 3)))
        self.ax = self.plot_widget.figure.subplots()

        layout.addLayout(self.left_panel)
        layout.addWidget(self.plot_widget)

        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(layout)

        # 🟦 Botones en UNA FILA
        self.buttons_layout = QHBoxLayout()
        botones = [
            ("📊 Diagrama", self.graficar),
            ("🧮 Calcular b0 y b1", self.calcular_betas),
            ("📈 Predicción", self.calcular_prediccion),
            ("📏 R²", self.calcular_r2),
            ("📎 Correlación r", self.calcular_correlacion),
            ("🔙 Volver", self.volver)  # <-- Botón Volver agregado aquí
        ]

        for texto, funcion in botones:
            btn = self.crear_boton(texto, funcion)
            self.buttons_layout.addWidget(btn)

        self.main_layout.addLayout(self.buttons_layout)
        self.setLayout(self.main_layout)

    def crear_boton(self, texto, funcion):
        btn = QPushButton(texto)
        btn.setFixedSize(200, 60)
        btn.setStyleSheet("""
            QPushButton {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                                  stop:0 #00BFFF, stop:1 #1E90FF);
                color: white;
                font-size: 16px;
                font-weight: bold;
                border-radius: 12px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #1C86EE;
            }
        """)
        btn.clicked.connect(funcion)
        return btn

    def obtener_datos(self):
        x_vals, y_vals = [], []
        for x, y in zip(self.x_inputs, self.y_inputs):
            try:
                if x.text() and y.text():
                    x_vals.append(float(x.text()))
                    y_vals.append(float(y.text()))
            except ValueError:
                continue
        return np.array(x_vals), np.array(y_vals)

    def calcular_betas(self):
        x, y = self.obtener_datos()
        if len(x) < 2:
            self.resultado_text.setText("Se requieren al menos 2 datos.")
            return
        b1 = np.cov(x, y, bias=True)[0][1] / np.var(x)
        b0 = np.mean(y) - b1 * np.mean(x)
        self.resultado_text.setText(f"b0 (intercepto): {b0:.2f}\nb1 (pendiente): {b1:.2f}")

    def calcular_prediccion(self):
        x, y = self.obtener_datos()
        try:
            x_pred = float(self.x_pred_input.text())
            b1 = np.cov(x, y, bias=True)[0][1] / np.var(x)
            b0 = np.mean(y) - b1 * np.mean(x)
            y_pred = b0 + b1 * x_pred
            self.resultado_text.setText(f"Predicción para X={x_pred}: Y={y_pred:.2f}")
        except Exception:
            self.resultado_text.setText("Error en predicción.")

    def calcular_r2(self):
        x, y = self.obtener_datos()
        y_mean = np.mean(y)
        b1 = np.cov(x, y, bias=True)[0][1] / np.var(x)
        b0 = np.mean(y) - b1 * np.mean(x)
        y_pred = b0 + b1 * x
        ss_tot = np.sum((y - y_mean)**2)
        ss_res = np.sum((y - y_pred)**2)
        r2 = 1 - ss_res / ss_tot
        self.resultado_text.setText(f"Coeficiente de determinación R² = {r2:.2f}")

    def calcular_correlacion(self):
        x, y = self.obtener_datos()
        r = np.corrcoef(x, y)[0, 1]
        self.resultado_text.setText(f"Coeficiente de correlación r = {r:.2f}")

    def graficar(self):
        x, y = self.obtener_datos()
        if len(x) < 2:
            self.resultado_text.setText("Se requieren al menos 2 datos para graficar.")
            return
        b1 = np.cov(x, y, bias=True)[0][1] / np.var(x)
        b0 = np.mean(y) - b1 * np.mean(x)
        y_pred = b0 + b1 * x
        self.ax.clear()
        self.ax.scatter(x, y, color='blue', label='Datos')
        self.ax.plot(x, y_pred, color='red', label=f'Regresión: Y = {b0:.2f} + {b1:.2f}X')
        self.ax.set_title('Regresión Lineal')
        self.ax.set_xlabel('Horas de estudio (X)')
        self.ax.set_ylabel('Calificación (Y)')
        self.ax.legend()
        self.plot_widget.draw()

    def volver(self):
        from Modulos.menu_general.menu_general import MenuGeneral
        self.menu = MenuGeneral()
        self.menu.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = RegresionLineal()
    ventana.show()
    sys.exit(app.exec_())
