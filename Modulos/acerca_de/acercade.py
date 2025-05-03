from PyQt5.QtWidgets import *  # También importa todos los widgets

# Se importan componentes del núcleo de PyQt5, como señales personalizadas y alineación
from PyQt5.QtCore import Qt

from Modulos.menu_general.menu_general import MenuGeneral



# Incluir un apartado “Acerca de” dentro del menú principal, que muestre
# información del autor, carrera, semestre, año académico, profesor y materia.
class AcercaDe(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Acerca de")  # Título de la ventana
        self.setGeometry(100, 100, 800, 600)  # Tamaño y posición de la ventana
        self.setStyleSheet("background-color: #0f111a; color: white; font-size: 18px;")  # Estilo de la ventana

        layout = QVBoxLayout()  # Layout principal (vertical)

        # Título de la sección
        titulo = QLabel("📘 Acerca del Proyecto")
        titulo.setAlignment(Qt.AlignCenter)  # Centra el título
        titulo.setStyleSheet("font-size: 30px; font-weight: bold; color: #00d2ff;")  # Estilo del título
        layout.addWidget(titulo)  # Agrega el título al layout

        # Contenido de la sección "Acerca de"
        contenido = QLabel(
            "<b>👨‍💻 Autor:</b> Gómez Molina José Andrés<br><br>"
            "<b>🎓 Carrera:</b> Ingeniería en Software<br><br>"
            "<b>📚 Semestre:</b> 6° Semestre<br><br>"
            "<b>📅 Año Académico:</b> 2025<br><br>"
            "<b>👨‍🏫 Profesor:</b> Ing. Isidro Fabricio Morales Torres<br><br>"
            "<b>🧠 Materia:</b> Modelos Matemáticos y Simulación"
        )

        # Estilo del contenido
        contenido.setStyleSheet("padding: 19px; font-size: 25px;")
        contenido.setAlignment(Qt.AlignLeft | Qt.AlignTop)  # Alineación del contenido a la izquierda y arriba
        contenido.setWordWrap(True)  # Permite que el texto se ajuste en caso de ser largo
        layout.addWidget(contenido)  # Agrega el contenido al layout

        # Botón para volver al menú
        boton_volver = QPushButton("Volver al Menú")
        boton_volver.setCursor(Qt.PointingHandCursor)  # Cambia el cursor a mano al pasar sobre el botón
        boton_volver.setStyleSheet(
            "background-color: #00d2ff; font-weight: bold; border-radius: 10px; padding: 10px; font-size: 18px;"
        )  # Estilo del botón
        boton_volver.clicked.connect(self.volver)  # Conecta el botón con la acción de volver
        layout.addWidget(boton_volver, alignment=Qt.AlignCenter)  # Agrega el botón al layout y lo centra

        # Asigna el layout a la ventana
        self.setLayout(layout)

    # Función para volver al menú general
    def volver(self):
        self.menu = MenuGeneral()  # Crea una instancia del menú principal
        self.menu.show()  # Muestra el menú principal
        self.close()  # Cierra la ventana actual
