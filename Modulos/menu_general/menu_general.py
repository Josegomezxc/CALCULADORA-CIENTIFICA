from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from utils.helpers import resource_path

class MenuGeneral(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculadora Científica")
        self.setGeometry(100, 100, 900, 600)
        self.setStyleSheet(self.estilos())

        # Module descriptions
        self.descriptions = {
            "Matrices": "Operaciones con matrices: suma, resta, multiplicación, determinantes, inversas y más.",
            "Polinomios": "Manipulación de polinomios: suma, resta, multiplicación,derivadas, integrales y más.",
            "Derivadas": "Cálculo simbólico de derivadas e integrales.",
            "Vectores": "Operaciones con vectores: producto punto, cruz, magnitud y más.",
            "Gráficas": "Visualización de funciones en 2D y 3D con herramientas interactivas.",
            "EDO": "Resolución de ecuaciones diferenciales ordinarias.",
            "Vectores Propios": "Cálculo de valores y vectores propios de matrices.",
            "Prob y Estadistica": "Análisis estadístico y cálculos de probabilidad.",
            "M. Matemático": "Simulación del modelo matemático SIR.",
            "Acerca De": "Información sobre la calculadora científica y sus creadores."
        }

        self.modulos = [
            ("Matrices", self.abrir_matrices),
            ("Polinomios", self.abrir_polinomios),
            ("Derivadas", self.abrir_derivadas),
            ("Vectores", self.abrir_vectores),
            ("Gráficas", self.abrir_graficas),
            ("EDO", self.abrir_edo),
            ("Vectores Propios", self.abrir_vectores_propios),
            ("Prob y Estadistica", self.abrir_estadistica),
            ("M. Matemático", self.abrir_MM),
            ("Regresion Lineal", self.abrir_regresion_lineal),
            ("Regresion Lineal M", self.abrir_regresion_lineal_multiple),
            ("Markov", self.abrir_Cadenas_Markov),
            ("Grafos", self.abrir_Grafos),
            ("Redes Petri", self.abrir_Redes_Petri),
            ("Algoritmos H-MH", self.abrir_Algoritmos_H_MH),
            ("Red Nuronal", self.abrir_Redes_Neuronales),
            ("Acerca De", self.abrir_acercade),
        ]

        # Main layout: horizontal for sidebar and content
        layout_principal = QHBoxLayout(self)
        layout_principal.setContentsMargins(0, 0, 20, 20)
        layout_principal.setSpacing(0)

        # Sidebar
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(260)  # Increased width for title visibility
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(20, 20, 20, 20)  # Adjusted margins
        sidebar_layout.setSpacing(12)
        sidebar_layout.setAlignment(Qt.AlignTop)

        # Sidebar title
        titulo = QLabel("Calculadora🖩")
        titulo.setObjectName("titulo")
        sidebar_layout.addWidget(titulo)

        # Scroll area for modules
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setSpacing(8)

        # Add module buttons
        for texto, funcion in self.modulos:
            button = self.crear_boton_modulo(texto, funcion)
            # Connect hover events
            button.enterEvent = lambda event, t=texto: self.show_description(t)
            button.leaveEvent = lambda event: self.clear_description()
            scroll_layout.addWidget(button)

        scroll_area.setWidgetsmartphone = QScrollArea()
        scroll_area.setWidget(scroll_content)
        sidebar_layout.addWidget(scroll_area)
        layout_principal.addWidget(sidebar)

        # Main content area
        content_area = QFrame()
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(40, 40, 40, 40)
        content_layout.setAlignment(Qt.AlignCenter)
        content_layout.setSpacing(20)

        # Welcome label
        welcome_label = QLabel("Selecciona un módulo para comenzar")
        welcome_label.setObjectName("welcome")
        welcome_label.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(welcome_label, alignment=Qt.AlignHCenter)

        # Description label
        self.description_label = QLabel("")
        self.description_label.setObjectName("description")
        self.description_label.setWordWrap(True)
        self.description_label.setFixedWidth(400)
        self.description_label.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(self.description_label, alignment=Qt.AlignHCenter)

        # Exit button
        boton_salir = QPushButton("Salir")
        boton_salir.setObjectName("botonSalir")
        boton_salir.setFixedWidth(200)
        boton_salir.setCursor(Qt.PointingHandCursor)
        boton_salir.clicked.connect(QApplication.quit)
        content_layout.addWidget(boton_salir, alignment=Qt.AlignHCenter)

        layout_principal.addWidget(content_area, stretch=1)

    def crear_boton_modulo(self, texto, funcion):
        button = QPushButton()
        button.setObjectName("botonModulo")
        button.setCursor(Qt.PointingHandCursor)
        button.setMinimumHeight(48)  # Changed to minimum height for flexibility
        button.clicked.connect(funcion)

        layout = QHBoxLayout(button)
        layout.setContentsMargins(12, 8, 12, 8)  # Added vertical padding
        layout.setSpacing(12)
        layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        # Icon
        imagen_label = QLabel()
        ruta_imagen = resource_path(f"images/{texto.lower()}.png")
        pixmap = QPixmap(ruta_imagen).scaled(28, 28, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        imagen_label.setPixmap(pixmap)
        imagen_label.setFixedSize(28, 28)

        # Text
        texto_label = QLabel(texto)
        texto_label.setObjectName("botonTexto")

        layout.addWidget(imagen_label)
        layout.addWidget(texto_label)
        layout.addStretch()

        return button

    def show_description(self, module_name):
        self.description_label.setText(self.descriptions.get(module_name, ""))

    def clear_description(self):
        self.description_label.setText("")

    def estilos(self):
        return """
        QWidget {
            background-color: #0f111a;
            color: #ffffff;
            font-family: 'Roboto', 'Inter', sans-serif;
        }

        QFrame#sidebar {
            background: qlineargradient(
                x1:0, y1:0, x2:0, y2:1,
                stop:0 #1e40af,
                stop:1 #60a5fa
            );
        }

        QLabel#titulo {
            font-size: 24px;
            font-weight: 700;
            color: #ffffff;
            padding: 15px 0;  /* Reduced padding for better fit */
            text-align: center;
            font-family: 'Roboto', 'Inter', sans-serif;
        }

        QPushButton#botonModulo {
            background: transparent;
            border: none;
            border-radius: 12px;  /* Increased for softer corners */
            color: #ffffff;
            font-size: 15px;
            text-align: left;
        }

        QPushButton#botonModulo:hover {
            background: rgba(255, 255, 255, 0.15);
        }

        QPushButton#botonModulo:pressed {
            background: rgba(255, 255, 255, 0.25);
        }

        QLabel#botonTexto {
            font-size: 15px;
            color: #ffffff;
            font-weight: 500;
            font-family: 'Roboto', 'Inter', sans-serif;
        }

        QLabel#welcome {
            font-size: 22px;
            font-weight: 500;
            color: #60a5fa;
            text-align: center;
            font-family: 'Roboto', 'Inter', sans-serif;
        }

        QLabel#description {
            font-size: 16px;
            font-weight: 400;
            color: #93c5fd;
            text-align: center;
            margin: 20px 0;
            max-width: 400px;
            font-family: 'Roboto', 'Inter', sans-serif;
        }

        QPushButton#botonSalir {
            background: qlineargradient(
                x1:0, y1:0, x2:1, y2:1,
                stop:0 #1e40af,
                stop:1 #60a5fa
            );
            color: #ffffff;
            font-size: 14px;
            font-weight: 500;
            border: none;
            padding: 10px 20px;
            border-radius: 10px;
            font-family: 'Roboto', 'Inter', sans-serif;
        }

        QPushButton#botonSalir:hover {
            background: qlineargradient(
                x1:0, y1:0, x2:1, y2:1,
                stop:0 #2563eb,
                stop:1 #93c5fd
            );
        }

        QScrollBar:vertical {
            background: transparent;
            width: 8px;
            margin: 0;
        }

        QScrollBar::handle:vertical {
            background: #93c5fd;
            border-radius: 4px;
            min-height: 20px;
        }

        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 0;
        }
        """

    # Métodos para abrir módulos
    def abrir_matrices(self):
        from Modulos.matrices.matrices import MenuMatrices 
        self.ventana = MenuMatrices()
        self.ventana.show()
        self.close()

    def abrir_polinomios(self):
        from Modulos.polinomios.polinomios import MenuPolinomios
        self.ventana = MenuPolinomios()
        self.ventana.show()
        self.close()

    def abrir_derivadas(self):
        from Modulos.calculo_simbolico.calculosimbolico import CalculoSimbolico
        self.ventana = CalculoSimbolico()
        self.ventana.show()
        self.close()

    def abrir_vectores(self):
        from Modulos.vectores.vectores import MenuVectores
        self.ventana = MenuVectores()
        self.ventana.show()
        self.close()

    def abrir_graficas(self):
        from Modulos.graficas.graficas import Graficas_2d_3d
        self.ventana = Graficas_2d_3d()
        self.ventana.show()
        self.close()
        
    def abrir_edo(self):
        from Modulos.EDO.EDO import EDO
        self.ventana = EDO()
        self.ventana.show()
        self.close()
        
    def abrir_vectores_propios(self):
        from Modulos.vectores_propios.vectores_propios import VectoresPropios 
        self.ventana = VectoresPropios()
        self.ventana.show()
        self.close()
    
    def abrir_estadistica(self):
        from Modulos.estadistica.estadistica import MenuEstadistica 
        self.ventana = MenuEstadistica()
        self.ventana.show()
        self.close()
        
    def abrir_MM(self):
        from Modulos.modelo_matematico.modelo_matematico import SimuladorSIR 
        self.ventana = SimuladorSIR()
        self.ventana.show()
        self.close()
        
    def abrir_regresion_lineal(self):
        from Modulos.regresion_lineal.regresion_lineal import RegresionLineal
        self.ventana = RegresionLineal()
        self.ventana.show()
        self.close()
        
    def abrir_regresion_lineal_multiple(self):
        from Modulos.regresion_lineal.regresion_lineal_multiple import RegresionLinealMultiple
        self.ventana = RegresionLinealMultiple()
        self.ventana.show()
        self.close()
        
    def abrir_Cadenas_Markov(self):
        from Modulos.Cadenas_Markov.Cadenas_Markov import CadenasMarkov
        self.ventana = CadenasMarkov()
        self.ventana.show()
        self.close()
        
    def abrir_Grafos(self):
        from Modulos.Grafos.Grafos import Grafos
        self.ventana = Grafos()
        self.ventana.show()
        self.close()
        
    def abrir_Redes_Petri(self):
        from Modulos.Redes_Petri.Redes_Petri import Redes_Petri
        self.ventana = Redes_Petri()
        self.ventana.show()
        self.close()
        
    def abrir_Algoritmos_H_MH(self):
        from Modulos.Algoritmos.Algoritmanos_Heuristicos import Algoritmos_Heuristicos
        self.ventana = Algoritmos_Heuristicos()
        self.ventana.show()
        self.close()
        
    def abrir_Redes_Neuronales(self):
        from Modulos.Redes_Neuronales.Redes_Neuronales import RedNeuronal
        self.ventana = RedNeuronal()
        self.ventana.show()
        self.close()
        
    def abrir_acercade(self):
        from Modulos.acerca_de.acercade import AcercaDe
        self.ventana = AcercaDe()
        self.ventana.show()
        self.close()