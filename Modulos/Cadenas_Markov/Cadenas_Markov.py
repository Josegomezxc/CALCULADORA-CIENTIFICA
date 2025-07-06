import sys
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QTableWidget, QTableWidgetItem, QSpinBox, QTextEdit
)
from PyQt5.QtCore import Qt

class CadenasMarkov(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cadenas de Markov Paso a Paso")
        self.setStyleSheet("background-color: #0F101A; color: white;")
        self.setGeometry(100, 100, 1000, 600)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        title = QLabel("🔁 Cadenas de Markov")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: cyan;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Controles superiores
        config_layout = QHBoxLayout()
        self.spin_dim = QSpinBox()
        self.spin_dim.setMinimum(2)
        self.spin_dim.setMaximum(10)
        self.spin_dim.setValue(3)
        self.spin_dim.setPrefix("Estados: ")
        self.spin_dim.valueChanged.connect(self.generar_tablas)
        self.spin_pasos = QSpinBox()
        self.spin_pasos.setMinimum(1)
        self.spin_pasos.setValue(3)
        self.spin_pasos.setPrefix("Pasos: ")
        config_layout.addWidget(self.spin_dim)
        config_layout.addWidget(self.spin_pasos)
        layout.addLayout(config_layout)

        self.tabla_P = QTableWidget()
        self.tabla_pi = QTableWidget()
        layout.addWidget(QLabel("Matriz de Transición P:"))
        layout.addWidget(self.tabla_P)
        layout.addWidget(QLabel("Vector de Estado Inicial π₀:"))
        layout.addWidget(self.tabla_pi)

        # Botones principales
        botones_layout = QHBoxLayout()
        self.btn_calcular = QPushButton("Calcular pasos")
        self.btn_calcular.clicked.connect(self.calcular_markov)
        self.btn_calcular.setStyleSheet(self.estilo_boton())

        self.btn_limpiar = QPushButton("🧹 Limpiar")
        self.btn_limpiar.clicked.connect(self.limpiar)
        self.btn_limpiar.setStyleSheet(self.estilo_boton())

        self.btn_volver = QPushButton("🔙 Volver")
        self.btn_volver.clicked.connect(self.volver)
        self.btn_volver.setStyleSheet(self.estilo_boton())

        botones_layout.addWidget(self.btn_calcular)
        botones_layout.addWidget(self.btn_limpiar)
        botones_layout.addWidget(self.btn_volver)
        layout.addLayout(botones_layout)

        self.resultado = QTextEdit()
        self.resultado.setReadOnly(True)
        self.resultado.setStyleSheet("background-color: #1e1e2f; color: lightgreen; font-size: 14px;")
        layout.addWidget(self.resultado)

        self.setLayout(layout)
        self.generar_tablas()

    def estilo_boton(self):
        return """
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
        """

    def generar_tablas(self):
        n = self.spin_dim.value()
        self.tabla_P.setRowCount(n)
        self.tabla_P.setColumnCount(n)
        self.tabla_pi.setRowCount(1)
        self.tabla_pi.setColumnCount(n)

        ejemplo_P = [
            [0.5, 0.3, 0.2],
            [0.1, 0.6, 0.3],
            [0.2, 0.3, 0.5]
        ]
        ejemplo_pi0 = [1, 0, 0]

        for i in range(n):
            for j in range(n):
                valor = str(ejemplo_P[i][j]) if i < 3 and j < 3 else "0.0"
                self.tabla_P.setItem(i, j, QTableWidgetItem(valor))
            valor_pi = str(ejemplo_pi0[i]) if i < 3 else "0.0"
            self.tabla_pi.setItem(0, i, QTableWidgetItem(valor_pi))

        self.resultado.clear()

    def leer_tabla(self, tabla):
        filas = tabla.rowCount()
        cols = tabla.columnCount()
        matriz = np.zeros((filas, cols))
        for i in range(filas):
            for j in range(cols):
                item = tabla.item(i, j)
                if item is not None:
                    try:
                        matriz[i, j] = float(item.text())
                    except ValueError:
                        return None
        return matriz

    def calcular_markov(self):
        P = self.leer_tabla(self.tabla_P)
        pi = self.leer_tabla(self.tabla_pi)

        if P is None or pi is None:
            self.resultado.setText("❌ Error en los datos.")
            return

        if not np.allclose(P.sum(axis=1), 1):
            self.resultado.setText("❌ Cada fila de la matriz debe sumar 1.")
            return

        pasos = self.spin_pasos.value()
        texto = f"π₀ = {pi.tolist()}\n"
        for n in range(1, pasos + 1):
            pi = pi @ P
            texto += f"\nπ{n} = {np.round(pi, 4).tolist()}"
        self.resultado.setText(texto)

    def limpiar(self):
        self.generar_tablas()
        self.resultado.clear()

    def volver(self):
        from Modulos.menu_general.menu_general import MenuGeneral
        self.menu = MenuGeneral()
        self.menu.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = CadenasMarkov()
    ventana.show()
    sys.exit(app.exec_())
