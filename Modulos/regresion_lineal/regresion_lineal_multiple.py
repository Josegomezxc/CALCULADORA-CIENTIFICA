import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QGridLayout, QTextEdit, QSpinBox
)
from PyQt5.QtCore import Qt
import numpy as np

class RegresionLinealMultiple(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Regresión Lineal Múltiple")
        self.setStyleSheet("background-color: #0F101A; color: white;")
        self.setGeometry(100, 100, 1000, 600)
        self.initUI()

    def initUI(self):
        self.left_panel = QVBoxLayout()

        title = QLabel("📊 REGRESIÓN LINEAL MÚLTIPLE")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: cyan;")
        self.left_panel.addWidget(title)

        subtitle = QLabel("Ingrese valores de X y Y por observación")
        subtitle.setStyleSheet("font-size: 10pt; color: #00BFFF;")
        self.left_panel.addWidget(subtitle)

        param_layout = QHBoxLayout()
        self.spin_vars = QSpinBox()
        self.spin_vars.setMinimum(2)
        self.spin_vars.setValue(2)
        self.spin_vars.setPrefix("X: ")
        self.spin_obs = QSpinBox()
        self.spin_obs.setMinimum(2)
        self.spin_obs.setValue(5)
        self.spin_obs.setPrefix("Obs: ")
        self.btn_generar = self.crear_boton("➕ Generar Inputs", self.generar_inputs)
        param_layout.addWidget(self.spin_vars)
        param_layout.addWidget(self.spin_obs)
        param_layout.addWidget(self.btn_generar)
        self.left_panel.addLayout(param_layout)

        self.inputs_grid = QGridLayout()
        self.left_panel.addLayout(self.inputs_grid)

        self.pred_label = QLabel("Valores para predicción (X1,X2...):")
        self.left_panel.addWidget(self.pred_label)
        self.x_pred_input = QLineEdit("6,80")
        self.left_panel.addWidget(self.x_pred_input)

        self.resultado_label = QLabel("Resultado:")
        self.left_panel.addWidget(self.resultado_label)
        self.resultado_text = QTextEdit()
        self.resultado_text.setReadOnly(True)
        self.resultado_text.setFixedHeight(80)
        self.left_panel.addWidget(self.resultado_text)

        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(self.left_panel)

        botones = [
            ("🧮 Calcular modelo", self.calcular_modelo),
            ("📈 Predecir Y", self.predecir),
            ("🔙 Volver", self.volver)
        ]
        self.buttons_layout = QHBoxLayout()
        for texto, funcion in botones:
            btn = self.crear_boton(texto, funcion)
            self.buttons_layout.addWidget(btn)
        self.main_layout.addLayout(self.buttons_layout)

        self.setLayout(self.main_layout)
        self.generar_inputs()

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

    def generar_inputs(self):
        for i in reversed(range(self.inputs_grid.count())):
            self.inputs_grid.itemAt(i).widget().deleteLater()

        self.x_inputs = []
        self.y_inputs = []

        obs = self.spin_obs.value()
        vars = self.spin_vars.value()

        ejemplo_x = [
            [2, 50],
            [4, 60],
            [6, 70],
            [8, 80],
            [10, 90]
        ]
        ejemplo_y = [130, 150, 170, 190, 210]

        for i in range(obs):
            row = []
            for j in range(vars):
                x_input = QLineEdit()
                x_input.setFixedWidth(60)
                valor_x = str(ejemplo_x[i][j]) if i < len(ejemplo_x) and j < len(ejemplo_x[i]) else ""
                x_input.setText(valor_x)
                self.inputs_grid.addWidget(QLabel(f"X{j+1}-{i+1}:"), i, j * 2)
                self.inputs_grid.addWidget(x_input, i, j * 2 + 1)
                row.append(x_input)
            y_input = QLineEdit()
            y_input.setFixedWidth(60)
            valor_y = str(ejemplo_y[i]) if i < len(ejemplo_y) else ""
            y_input.setText(valor_y)
            self.inputs_grid.addWidget(QLabel(f"Y{i+1}:"), i, vars * 2)
            self.inputs_grid.addWidget(y_input, i, vars * 2 + 1)
            self.x_inputs.append(row)
            self.y_inputs.append(y_input)

    def obtener_datos(self):
        datos_x, datos_y = [], []
        for fila_x, y in zip(self.x_inputs, self.y_inputs):
            try:
                fila = [float(x.text()) for x in fila_x]
                y_val = float(y.text())
                datos_x.append(fila)
                datos_y.append(y_val)
            except ValueError:
                continue
        return np.array(datos_x), np.array(datos_y)

    def calcular_modelo(self):
        X, y = self.obtener_datos()
        if len(X) < 2 or X.shape[1] < 1:
            self.resultado_text.setText("Se necesitan mínimo 2 observaciones y 1 variable.")
            return
        try:
            X_b = np.hstack([np.ones((X.shape[0], 1)), X])
            beta = np.linalg.pinv(X_b.T @ X_b) @ X_b.T @ y.reshape(-1, 1)

            self.beta = beta.flatten()
            y_pred = X_b @ beta
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            ss_res = np.sum((y - y_pred.flatten()) ** 2)
            r2 = 1 - ss_res / ss_tot

            ecuacion = f"Y = {self.beta[0]:.4f} " + " ".join(
                [f"+ ({b:.4f})X{i+1}" for i, b in enumerate(self.beta[1:])]
            )
            self.resultado_text.setText(f"{ecuacion}\nR² = {r2:.4f}")
        except Exception as e:
            self.resultado_text.setText("Error en cálculo: " + str(e))

    def predecir(self):
        try:
            if not hasattr(self, "beta"):
                self.resultado_text.setText("Primero debes calcular el modelo.")
                return
            valores = list(map(float, self.x_pred_input.text().split(",")))
            valores = [1.0] + valores
            y_pred = np.dot(self.beta, valores)
            self.resultado_text.setText(f"Predicción: Y = {y_pred:.4f}")
        except Exception as e:
            self.resultado_text.setText("Error en predicción: " + str(e))

    def volver(self):
        from Modulos.menu_general.menu_general import MenuGeneral
        self.menu = MenuGeneral()
        self.menu.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = RegresionLinealMultiple()
    ventana.show()
    sys.exit(app.exec_())
