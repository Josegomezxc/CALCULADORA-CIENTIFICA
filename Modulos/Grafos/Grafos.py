import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QSpinBox, QTextEdit, QGraphicsView, QGraphicsScene,
    QComboBox, QTabWidget, QTableWidget, QTableWidgetItem
)
from PyQt5.QtGui import QPen, QBrush, QPainter
from PyQt5.QtCore import Qt, QPointF
import numpy as np
import math

class Grafos(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Módulo de Grafos")
        self.setGeometry(100, 100, 1200, 700)
        self.setStyleSheet("background-color: #0F101A; color: white;")
        self.initUI()

    def initUI(self):
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("QTabBar::tab { font-weight: bold; font-size: 14px; padding: 10px; }")

        self.tab_manual = QWidget()
        self.tab_matriz = QWidget()

        self.tabs.addTab(self.tab_manual, "🎯 Ingreso Manual")
        self.tabs.addTab(self.tab_matriz, "🧬 Desde Matriz")

        self.init_manual_tab()
        self.init_matriz_tab()

        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        self.setLayout(layout)

    def init_manual_tab(self):
        layout = QHBoxLayout()
        self.left_panel = QVBoxLayout()

        title = QLabel("🔷 MÓDULO DE GRAFOS (Manual)")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: cyan;")
        self.left_panel.addWidget(title)

        config_layout = QHBoxLayout()
        self.nodo_spin = QSpinBox()
        self.nodo_spin.setMinimum(2)
        self.nodo_spin.setMaximum(15)
        self.nodo_spin.setPrefix("Nodos: ")
        config_layout.addWidget(self.nodo_spin)

        self.tipo_combo = QComboBox()
        self.tipo_combo.addItems(["No Dirigido", "Dirigido"])
        self.tipo_combo.setStyleSheet("color: White; font-weight: bold; border: 1px solid white; padding: 4px;")
        config_layout.addWidget(self.tipo_combo)

        config_layout.addWidget(self.crear_boton("➕ Generar Nodos", self.generar_nodos))
        config_layout.addWidget(self.crear_boton("🧹 Limpiar", self.limpiar))
        config_layout.addWidget(self.crear_boton("🔙 Volver", self.volver))
        self.left_panel.addLayout(config_layout)

        self.matriz_text = QTextEdit()
        self.matriz_text.setReadOnly(True)
        self.matriz_text.setStyleSheet("font-family: Consolas; font-size: 12pt;")
        self.left_panel.addWidget(self.matriz_text)

        layout.addLayout(self.left_panel)

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.Antialiasing)
        self.view.setStyleSheet("background-color: white;")
        self.view.setFixedSize(700, 650)
        layout.addWidget(self.view)

        self.tab_manual.setLayout(layout)
        self.nodos = []
        self.aristas = []
        self.clicks = []

    def init_matriz_tab(self):
        layout = QHBoxLayout()
        left_panel = QVBoxLayout()

        info = QLabel("📜 Ingrese la matriz de incidencia (1, -1, 0):")
        info.setStyleSheet("font-size: 16px; color: cyan;")
        left_panel.addWidget(info)

        self.table = QTableWidget(4, 5)
        self.table.setStyleSheet("background-color: white; color: black;")
        valores = [[1, 0, 0, 0, 1], [-1, 1, 0, 0, 0], [0, -1, 1, 0, 0], [0, 0, -1, -1, -1]]
        for i in range(4):
            for j in range(5):
                self.table.setItem(i, j, QTableWidgetItem(str(valores[i][j])))
        left_panel.addWidget(self.table)

        left_panel.addWidget(self.crear_boton("📊 Generar Grafo", self.generar_desde_matriz))
        layout.addLayout(left_panel)

        self.scene_matriz = QGraphicsScene()
        self.view_matriz = QGraphicsView(self.scene_matriz)
        self.view_matriz.setRenderHint(QPainter.Antialiasing)
        self.view_matriz.setStyleSheet("background-color: white;")
        self.view_matriz.setFixedSize(700, 650)
        layout.addWidget(self.view_matriz)

        self.tab_matriz.setLayout(layout)

    def crear_boton(self, texto, funcion):
        btn = QPushButton(texto)
        btn.setFixedSize(160, 70)
        btn.setStyleSheet("""
            QPushButton {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #00BFFF, stop:1 #1E90FF);
                color: white; font-size: 14px; font-weight: bold; border-radius: 12px;
            }
            QPushButton:hover {
                background-color: #1C86EE;
            }
        """)
        btn.clicked.connect(funcion)
        return btn

    def generar_nodos(self):
        self.scene.clear()
        self.nodos.clear()
        self.aristas.clear()
        self.clicks.clear()
        self.matriz_text.clear()

        n = self.nodo_spin.value()
        radio = 250
        center = QPointF(330, 300)

        for i in range(n):
            angle = 2 * math.pi * i / n
            x = center.x() + radio * math.cos(angle)
            y = center.y() + radio * math.sin(angle)
            nodo = self.scene.addEllipse(x, y, 40, 40, QPen(Qt.black), QBrush(Qt.green))
            nodo.setData(0, i)
            self.scene.addText(str(i+1)).setPos(x + 12, y + 5)
            self.nodos.append((nodo, QPointF(x + 20, y + 20)))

        self.view.viewport().installEventFilter(self)

    def eventFilter(self, source, event):
        if event.type() == event.MouseButtonPress:
            click_pos = self.view.mapToScene(event.pos())
            for i, (nodo, centro) in enumerate(self.nodos):
                if (click_pos - centro).manhattanLength() < 25:
                    self.clicks.append(i)
                    if len(self.clicks) == 2:
                        self.dibujar_arista(self.clicks[0], self.clicks[1])
                        self.clicks.clear()
                    break
        return super().eventFilter(source, event)

    def dibujar_arista(self, i, j):
        p1 = self.nodos[i][1]
        p2 = self.nodos[j][1]
        dirigido = self.tipo_combo.currentText() == "Dirigido"
        pen = QPen(Qt.red if dirigido else Qt.darkBlue, 2)
        self.scene.addLine(p1.x(), p1.y(), p2.x(), p2.y(), pen)
        self.aristas.append((i, j))

        if dirigido:
            dx = p2.x() - p1.x()
            dy = p2.y() - p1.y()
            angle = math.atan2(dy, dx)
            arrow_size = 12
            px = p2.x() - arrow_size * math.cos(angle)
            py = p2.y() - arrow_size * math.sin(angle)
            self.scene.addLine(px, py, px - 5 * math.cos(angle + math.pi/6), py - 5 * math.sin(angle + math.pi/6), pen)
            self.scene.addLine(px, py, px - 5 * math.cos(angle - math.pi/6), py - 5 * math.sin(angle - math.pi/6), pen)

        self.generar_matrices()

    def generar_matrices(self):
        n = len(self.nodos)
        m = len(self.aristas)
        dirigido = self.tipo_combo.currentText() == "Dirigido"
        ady = np.zeros((n, n), dtype=int)
        inc = np.zeros((n, m), dtype=int)

        for k, (i, j) in enumerate(self.aristas):
            if dirigido:
                ady[i][j] = 1
                inc[i][k] = -1
                inc[j][k] = 1
            else:
                ady[i][j] = ady[j][i] = 1
                inc[i][k] = inc[j][k] = 1

        texto = "📌 Matriz de Adyacencia:\n" + str(ady) + "\n\n"
        texto += "📌 Matriz de Incidencia:\n" + str(inc)

        if dirigido:
            texto += "\n\n" + self.calcular_grados_dirigido(self.aristas, n)

        self.matriz_text.setText(texto)

    def calcular_grados_dirigido(self, aristas, n):
        grado_mas = np.zeros(n, dtype=int)
        grado_menos = np.zeros(n, dtype=int)
        for origen, destino in aristas:
            grado_menos[origen] += 1
            grado_mas[destino] += 1
        gtotal = grado_mas + grado_menos
        gneto = grado_mas - grado_menos
        tabla = "📌 Tabla de Grados del Grafo Dirigido:\n"
        tabla += f"{'Nodo':<8}{'Grado +':<10}{'Grado -':<10}{'Total':<10}{'Neto':<10}\n"
        for idx in range(n):
            tabla += f"{'g(' + str(idx+1) + ')':<8}{grado_mas[idx]:<10}{grado_menos[idx]:<10}{gtotal[idx]:<10}{gneto[idx]:<10}\n"
        return tabla

    def generar_desde_matriz(self):
        self.scene_matriz.clear()
        nodos = self.table.rowCount()
        aristas = self.table.columnCount()
        inc = np.zeros((nodos, aristas), dtype=int)
        for i in range(nodos):
            for j in range(aristas):
                item = self.table.item(i, j)
                if item and item.text().strip():
                    try:
                        inc[i][j] = int(item.text())
                    except ValueError:
                        pass
        radio = 250
        center = QPointF(330, 300)
        posiciones = []
        for i in range(nodos):
            angle = 2 * math.pi * i / nodos
            x = center.x() + radio * math.cos(angle)
            y = center.y() + radio * math.sin(angle)
            self.scene_matriz.addEllipse(x, y, 40, 40, QPen(Qt.black), QBrush(Qt.green))
            self.scene_matriz.addText(str(i+1)).setPos(x + 12, y + 5)
            posiciones.append(QPointF(x + 20, y + 20))
        for j in range(aristas):
            origen = destino = None
            for i in range(nodos):
                if inc[i][j] == -1:
                    origen = i
                elif inc[i][j] == 1:
                    destino = i
            if origen is not None and destino is not None:
                p1 = posiciones[origen]
                p2 = posiciones[destino]
                pen = QPen(Qt.red, 2)
                self.scene_matriz.addLine(p1.x(), p1.y(), p2.x(), p2.y(), pen)
                dx = p2.x() - p1.x()
                dy = p2.y() - p1.y()
                angle = math.atan2(dy, dx)
                arrow_size = 12
                px = p2.x() - arrow_size * math.cos(angle)
                py = p2.y() - arrow_size * math.sin(angle)
                self.scene_matriz.addLine(px, py, px - 5 * math.cos(angle + math.pi/6), py - 5 * math.sin(angle + math.pi/6), pen)
                self.scene_matriz.addLine(px, py, px - 5 * math.cos(angle - math.pi/6), py - 5 * math.sin(angle - math.pi/6), pen)

    def limpiar(self):
        self.scene.clear()
        self.matriz_text.clear()
        self.nodos.clear()
        self.aristas.clear()
        self.clicks.clear()

    def volver(self):
        from Modulos.menu_general.menu_general import MenuGeneral
        self.menu = MenuGeneral()
        self.menu.show()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = Grafos()
    ventana.show()
    sys.exit(app.exec_())
