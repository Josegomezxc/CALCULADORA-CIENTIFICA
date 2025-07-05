import sys
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QGraphicsScene, QGraphicsView, QLineEdit, QSpinBox, QTextEdit
)
from PyQt5.QtGui import QPen, QBrush
from PyQt5.QtCore import Qt, QPointF

class Redes_Petri(QWidget):
    def __init__(self, volver_callback=None):
        super().__init__()
        self.setWindowTitle("Red de Petri")
        self.setGeometry(100, 100, 1100, 600)
        self.setStyleSheet("background-color: #101820; color: white;")
        self.volver_callback = volver_callback
        self.places = {}
        self.transitions = {}
        self.arcs = []
        self.clicks = []
        self.initUI()

    def initUI(self):
        main_layout = QHBoxLayout()

        left_panel = QVBoxLayout()
        title = QLabel("🔄 Red de Petri")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: cyan;")
        left_panel.addWidget(title)

        self.input_place = QLineEdit()
        self.input_place.setPlaceholderText("Nombre del lugar (ej. P1)")
        left_panel.addWidget(self.input_place)

        self.input_tokens = QSpinBox()
        self.input_tokens.setPrefix("Tokens: ")
        self.input_tokens.setMaximum(100)
        left_panel.addWidget(self.input_tokens)

        btn_add_place = QPushButton("➕ Añadir Lugar")
        btn_add_place.clicked.connect(self.add_place)
        left_panel.addWidget(btn_add_place)

        self.input_transition = QLineEdit()
        self.input_transition.setPlaceholderText("Nombre de transición (ej. T1)")
        left_panel.addWidget(self.input_transition)

        btn_add_transition = QPushButton("⚙️ Añadir Transición")
        btn_add_transition.clicked.connect(self.add_transition)
        left_panel.addWidget(btn_add_transition)

        self.btn_disparar = QPushButton("🔥 Calcular M1, M2,...")
        self.btn_disparar.clicked.connect(self.disparar)
        left_panel.addWidget(self.btn_disparar)

        self.btn_limpiar = QPushButton("🧹 Limpiar Todo")
        self.btn_limpiar.clicked.connect(self.limpiar)
        left_panel.addWidget(self.btn_limpiar)

        self.btn_volver = QPushButton("🔙 Volver")
        self.btn_volver.clicked.connect(self.volver)
        left_panel.addWidget(self.btn_volver)

        self.status_output = QTextEdit()
        self.status_output.setReadOnly(True)
        self.status_output.setStyleSheet("background-color: white; color: black;")
        left_panel.addWidget(self.status_output)

        main_layout.addLayout(left_panel)

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setStyleSheet("background-color: white;")
        self.view.setFixedSize(600, 550)
        main_layout.addWidget(self.view)
        self.setLayout(main_layout)

        self.view.viewport().installEventFilter(self)

    def add_place(self):
        name = self.input_place.text().strip()
        tokens = self.input_tokens.value()
        if name and name not in self.places:
            pos = QPointF(100 + len(self.places) * 100, 100)
            ellipse = self.scene.addEllipse(pos.x(), pos.y(), 40, 40, QPen(Qt.black), QBrush(Qt.green))
            text = self.scene.addText(name)
            text.setPos(pos.x() + 5, pos.y() + 10)
            self.places[name] = {"pos": pos, "tokens": tokens, "center": pos + QPointF(20, 20)}
            self.input_place.clear()
            self.update_status()

    def add_transition(self):
        name = self.input_transition.text().strip()
        if name and name not in self.transitions:
            pos = QPointF(100 + len(self.transitions) * 100, 250)
            rect = self.scene.addRect(pos.x(), pos.y(), 15, 60, QPen(Qt.black), QBrush(Qt.blue))
            text = self.scene.addText(name)
            text.setPos(pos.x() - 5, pos.y() + 65)
            self.transitions[name] = {"pos": pos, "center": pos + QPointF(7, 30)}
            self.input_transition.clear()
            self.update_status()

    def eventFilter(self, source, event):
        if event.type() == event.MouseButtonPress:
            click_pos = self.view.mapToScene(event.pos())
            for name, data in list(self.places.items()) + list(self.transitions.items()):
                center = data["center"]
                if (click_pos - center).manhattanLength() < 25:
                    self.clicks.append((name, center))
                    if len(self.clicks) == 2:
                        self.crear_arco(self.clicks[0], self.clicks[1])
                        self.clicks.clear()
                    break
        return super().eventFilter(source, event)

    def crear_arco(self, origen_data, destino_data):
        origen, p1 = origen_data
        destino, p2 = destino_data

        if (origen in self.places and destino in self.transitions) or (origen in self.transitions and destino in self.places):
            self.scene.addLine(p1.x(), p1.y(), p2.x(), p2.y(), QPen(Qt.red, 2))

            dx, dy = p2.x() - p1.x(), p2.y() - p1.y()
            angle = np.arctan2(dy, dx)
            arrow_size = 10
            arrow_x = p2.x() - arrow_size * np.cos(angle)
            arrow_y = p2.y() - arrow_size * np.sin(angle)

            self.scene.addLine(arrow_x, arrow_y,
                               arrow_x - 5 * np.cos(angle + np.pi / 6),
                               arrow_y - 5 * np.sin(angle + np.pi / 6),
                               QPen(Qt.red, 2))
            self.scene.addLine(arrow_x, arrow_y,
                               arrow_x - 5 * np.cos(angle - np.pi / 6),
                               arrow_y - 5 * np.sin(angle - np.pi / 6),
                               QPen(Qt.red, 2))

            self.arcs.append((origen, destino))
            self.update_status()

    def disparar(self):
        lugares = list(self.places.keys())
        transiciones = list(self.transitions.keys())
        num_places = len(lugares)
        num_trans = len(transiciones)

        pre = np.zeros((num_places, num_trans), dtype=int)
        post = np.zeros((num_places, num_trans), dtype=int)

        for i, p in enumerate(lugares):
            for j, t in enumerate(transiciones):
                if (p, t) in self.arcs:
                    pre[i][j] += 1
                if (t, p) in self.arcs:
                    post[i][j] += 1

        T = post - pre
        M = np.array([self.places[p]["tokens"] for p in lugares], dtype=int)
        log = "🔰 Marcado Inicial M0 = " + str(M.tolist()) + "\n"
        log += "📌 Matriz Pre:\n" + str(pre) + "\n"
        log += "📌 Matriz Post:\n" + str(post) + "\n"
        log += "📌 Matriz T (Post - Pre):\n" + str(T) + "\n\n"

        for i in range(num_trans):
            M = M + T[:, i]
            log += f"🔥 M{i+1} = M{i} + T{i+1} = {M.tolist()}\n"

        self.status_output.setText(log)

    def limpiar(self):
        self.scene.clear()
        self.places.clear()
        self.transitions.clear()
        self.arcs.clear()
        self.clicks.clear()
        self.status_output.clear()

    def volver(self):
        from Modulos.menu_general.menu_general import MenuGeneral
        self.menu = MenuGeneral()
        self.menu.show()
        self.close()

    def update_status(self):
        texto = "📌 Tokens actuales:\n"
        for p in self.places:
            texto += f"{p}: {self.places[p]['tokens']} tokens\n"
        self.status_output.setText(texto)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = Redes_Petri()
    ventana.show()
    sys.exit(app.exec_())
