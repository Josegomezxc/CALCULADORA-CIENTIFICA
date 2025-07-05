import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QLineEdit, QTableWidget, QTableWidgetItem, QTextEdit
)
from PyQt5.QtCore import Qt

class RedNeuronal(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🧠 Perceptrón - Función AND de x1·x2")
        self.setGeometry(100, 100, 900, 500)
        self.setStyleSheet("background-color:#101820; color:white; font-size:14px; font-family:Consolas;")
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Tabla verdad
        self.tabla = QTableWidget(4, 4)
        self.tabla.setHorizontalHeaderLabels(["X0", "X1", "X2", "X1·X2"])
        datos = [[-1, 1, 1, 1], [-1, 1, -1, 1], [-1, -1, 1, 1], [-1, -1, -1, -1]]
        for i, fila in enumerate(datos):
            for j, val in enumerate(fila):
                item = QTableWidgetItem(str(val))
                item.setTextAlignment(Qt.AlignCenter)
                self.tabla.setItem(i, j, item)
        layout.addWidget(self.tabla)

        # Entradas de pesos y eta
        fila_pesos = QHBoxLayout()
        self.w0 = QLineEdit("0"); self.w1 = QLineEdit("0"); self.w2 = QLineEdit("0"); self.eta = QLineEdit("0.5")
        for w in [self.w0, self.w1, self.w2, self.eta]:
            w.setFixedWidth(70); fila_pesos.addWidget(w)
        self.btn_entrenar = QPushButton("► Entrenar"); self.btn_entrenar.clicked.connect(self.entrenar)
        self.btn_reset = QPushButton("🔁 Reset"); self.btn_reset.clicked.connect(self.resetear)
        self.btn_reset = QPushButton("🔙 Volver"); self.btn_reset.clicked.connect(self.volver)
        fila_pesos.addWidget(self.btn_entrenar); fila_pesos.addWidget(self.btn_reset)
        layout.addLayout(fila_pesos)

        # Área de resultados
        self.resultados = QTextEdit(); self.resultados.setReadOnly(True)
        layout.addWidget(self.resultados)

        self.setLayout(layout)

    def entrenar(self):
        try:
            w0 = float(self.w0.text())
            w1 = float(self.w1.text())
            w2 = float(self.w2.text())
            n = float(self.eta.text())
        except ValueError:
            self.resultados.setText("❌ Ingresa números válidos en los pesos y η.")
            return

        patrones = [[-1, 1, 1], [-1, 1, -1], [-1, -1, 1], [-1, -1, -1]]
        deseado = [1, 1, 1, -1]

        self.resultados.clear()
        epoca = 0
        aprendido = False

        while not aprendido and epoca < 100:
            epoca += 1
            self.resultados.append(f"🌐 Época {epoca}")
            errores = 0

            for i in range(len(patrones)):
                x0, x1, x2 = patrones[i]
                d = deseado[i]
                z = w0*x0 + w1*x1 + w2*x2
                y = 1 if z >= 0 else -1
                error = d - y

                self.resultados.append(f"Patrón {i+1}: z={z:.2f}, y={y}, d={d}, error={error}")

                if error != 0:
                    w0 += n * error * x0
                    w1 += n * error * x1
                    w2 += n * error * x2
                    errores += 1
                    self.resultados.append(f"🛠 Ajuste pesos ➜ w0={w0:.2f}, w1={w1:.2f}, w2={w2:.2f}")
                self.resultados.append("")

            if errores == 0:
                aprendido = True
                self.resultados.append("✅ ¡Red entrenada correctamente!")

        if not aprendido:
            self.resultados.append("⚠️ No se logró aprender en 100 épocas.")

        self.w0.setText(str(round(w0, 3)))
        self.w1.setText(str(round(w1, 3)))
        self.w2.setText(str(round(w2, 3)))

    def resetear(self):
        self.w0.setText("0")
        self.w1.setText("0")
        self.w2.setText("0")
        self.eta.setText("0.5")
        self.resultados.clear()

    def volver(self):
        from Modulos.menu_general.menu_general import MenuGeneral
        self.menu = MenuGeneral()
        self.menu.show()
        self.close()
