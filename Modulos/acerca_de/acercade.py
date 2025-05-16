from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFrame
from PyQt5.QtCore import Qt
from Modulos.menu_general.menu_general import MenuGeneral

class AcercaDe(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Acerca de")
        self.setGeometry(100, 100, 800, 600)
        # Fondo con degradado
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #0a0c15, stop: 1 #1e2a44
                );
                color: white;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 18px;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)  # Márgenes externos
        layout.setSpacing(20)  # Espaciado entre elementos

        # Título
        titulo = QLabel("📘 Acerca del Proyecto")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("""
            font-size: 34px;
            font-weight: bold;
            color: #00d2ff;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
        """)
        layout.addWidget(titulo)

        # Contenedor de contenido
        contenedor = QFrame()
        contenedor.setStyleSheet("""
            QFrame {
                background-color: rgba(30, 46, 68, 0.9);
                border-radius: 15px;
                padding: 20px;
                box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.3);
            }
        """)
        contenedor_layout = QVBoxLayout(contenedor)
        contenedor_layout.setContentsMargins(15, 15, 15, 15)

        # Contenido
        contenido = QLabel(
            "<b>👨‍💻 Autor:</b> Gómez Molina José Andrés<br>"
            "<b>🎓 Carrera:</b> Ingeniería en Software<br>"
            "<b>📚 Semestre:</b> 6° Semestre<br>"
            "<b>📅 Año Académico:</b> 2025<br>"
            "<b>👨‍🏫 Profesor:</b> Ing. Isidro Fabricio Morales Torres<br>"
            "<b>🧠 Materia:</b> Modelos Matemáticos y Simulación"
        )
        contenido.setStyleSheet("""
            font-size: 22px;
            line-height: 1.5;
            color: #e0e0e0;
        """)
        contenido.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        contenido.setWordWrap(True)
        contenedor_layout.addWidget(contenido)
        layout.addWidget(contenedor)

        # Espaciador para centrar verticalmente
        layout.addStretch()

        # Botón Volver
        boton_volver = QPushButton("Volver al Menú")
        boton_volver.setCursor(Qt.PointingHandCursor)
        boton_volver.setStyleSheet("""
            QPushButton {
                background-color: #00d2ff;
                color: white;
                font-weight: bold;
                font-size: 18px;
                border-radius: 12px;
                padding: 12px 24px;
                border: none;
                box-shadow: 3px 3px 10px rgba(0, 0, 0, 0.3);
                transition: all 0.3s ease;
            }
            QPushButton:hover {
                background-color: #33eaff;
                transform: scale(1.05);
                box-shadow: 5px 5px 15px rgba(0, 210, 255, 0.5);
            }
            QPushButton:pressed {
                background-color: #0099cc;
                box-shadow: inset 2px 2px 5px rgba(0, 0, 0, 0.2);
            }
        """)
        boton_volver.clicked.connect(self.volver)
        layout.addWidget(boton_volver, alignment=Qt.AlignCenter)

        # Espaciador inferior
        layout.addStretch()

        self.setLayout(layout)

    def volver(self):
        self.menu = MenuGeneral()
        self.menu.show()
        self.close()