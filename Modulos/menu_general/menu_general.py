from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from utils.helpers import resource_path

class MenuGeneral(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🧠 Calculadora Científica")
        self.setGeometry(100, 100, 900, 600)
        self.setStyleSheet(self.estilos())

        self.modulos = [
            ("Matrices", self.abrir_matrices),
            ("Polinomios", self.abrir_polinomios),
            ("Derivadas", self.abrir_derivadas),
            ("Vectores", self.abrir_vectores),
            ("Gráficas", self.abrir_graficas),
            ("EDO", self.abrir_edo),
            ("Vectores Propios", self.abrir_vectores_propios),
            ("Prob y Estadistica", self.abrir_estadistica),
            # ("Num Aleatorios", self.abrir_numeros_aleatorios),
            ("M. Matemático", self.abrir_MM),
            ("Acerca De", self.abrir_acercade),
        ]

        self.pagina_actual = 0
        self.modulos_por_pagina = 6

        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(40, 40, 40, 40)
        layout_principal.setSpacing(30)

        titulo = QLabel("🧠 Calculadora Científica")
        titulo.setObjectName("titulo")
        layout_principal.addWidget(titulo)

        # Layout horizontal para flechas y grid
        contenedor_horizontal = QHBoxLayout()
        contenedor_horizontal.setContentsMargins(0, 0, 0, 0)
        contenedor_horizontal.setSpacing(0)

        # Botón flecha izquierda
        self.boton_izquierda = QPushButton()
        self.boton_izquierda.setFixedSize(80, 200)
        self.crear_boton_con_imagen(self.boton_izquierda, "flecha_izquierda")
        self.boton_izquierda.clicked.connect(self.pagina_anterior)

        # Botón flecha derecha
        self.boton_derecha = QPushButton()
        self.boton_derecha.setFixedSize(80, 200)
        self.crear_boton_con_imagen(self.boton_derecha, "flecha_derecha")
        self.boton_derecha.clicked.connect(self.pagina_siguiente)

        # Grid para módulos
        self.grid_modulos = QGridLayout()
        self.grid_modulos.setSpacing(30)
        self.grid_modulos.setAlignment(Qt.AlignCenter)

        contenedor_horizontal.addWidget(self.boton_izquierda, alignment=Qt.AlignVCenter)
        contenedor_horizontal.addLayout(self.grid_modulos)
        contenedor_horizontal.addWidget(self.boton_derecha, alignment=Qt.AlignVCenter)

        layout_principal.addLayout(contenedor_horizontal)

        boton_salir = QPushButton("Salir")
        boton_salir.setObjectName("botonVolver")
        boton_salir.setFixedWidth(240)
        boton_salir.setCursor(Qt.PointingHandCursor)
        boton_salir.clicked.connect(QApplication.quit)
        layout_principal.addWidget(boton_salir, alignment=Qt.AlignCenter)

        self.actualizar_grid()

    def crear_boton_con_imagen(self, boton: QPushButton, nombre_imagen: str):
        # Crea QLabel con imagen usando resource_path y la pone dentro del botón
        ruta_imagen = resource_path(f"images/{nombre_imagen}.png")
        pixmap = QPixmap(ruta_imagen).scaled(64, 128, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        label_imagen = QLabel()
        label_imagen.setPixmap(pixmap)
        label_imagen.setAlignment(Qt.AlignCenter)

        boton.setLayout(QVBoxLayout())
        boton.layout().addWidget(label_imagen)
        boton.setCursor(Qt.PointingHandCursor)
        boton.setStyleSheet("border:none; background:transparent;")

    def actualizar_grid(self):
        # Limpia grid antes de llenar
        for i in reversed(range(self.grid_modulos.count())):
            widget = self.grid_modulos.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        inicio = self.pagina_actual * self.modulos_por_pagina
        fin = inicio + self.modulos_por_pagina
        modulos_pagina = self.modulos[inicio:fin]

        row, col = 0, 0
        for texto, funcion in modulos_pagina:
            tarjeta = self.crear_tarjeta(texto, funcion)
            self.grid_modulos.addWidget(tarjeta, row, col)
            col += 1
            if col >= 3:
                col = 0
                row += 1

        self.boton_izquierda.setEnabled(self.pagina_actual > 0)
        self.boton_derecha.setEnabled(fin < len(self.modulos))

    def pagina_siguiente(self):
        if (self.pagina_actual + 1) * self.modulos_por_pagina < len(self.modulos):
            self.pagina_actual += 1
            self.actualizar_grid()

    def pagina_anterior(self):
        if self.pagina_actual > 0:
            self.pagina_actual -= 1
            self.actualizar_grid()

    def crear_tarjeta(self, texto, funcion):
        tarjeta = QFrame()
        tarjeta.setObjectName("tarjeta")
        tarjeta.setFixedSize(240, 160)

        layout = QVBoxLayout(tarjeta)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignCenter)

        imagen_label = QLabel()
        ruta_imagen = resource_path(f"images/{texto.lower()}.png")
        pixmap = QPixmap(ruta_imagen).scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        imagen_label.setPixmap(pixmap)
        imagen_label.setAlignment(Qt.AlignCenter)

        boton = QPushButton(texto)
        boton.setObjectName("botonTarjeta")
        boton.setCursor(Qt.PointingHandCursor)
        boton.setFixedSize(180, 60)
        boton.clicked.connect(funcion)

        layout.addWidget(imagen_label)
        layout.addSpacing(10)
        layout.addWidget(boton)

        return tarjeta

    def estilos(self):
        return """
        QWidget {
            background-color: #0f111a;
            color: #f1f1f1;
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 15px;
        }

        QLabel#titulo {
            font-size: 30px;
            font-weight: bold;
            padding: 20px;
            background-color: #1a1d2e;
            border-bottom: 3px solid #00d2ff;
            color: #00d2ff;
            qproperty-alignment: AlignCenter;
        }

        QFrame#tarjeta {
            background-color: transparent;
            border-radius: 20px;
            border: 1px solid #2e86de;
        }

        QPushButton#botonTarjeta {
            background-color: qlineargradient(
                x1:0, y1:0, x2:1, y2:1,
                stop:0 #00d2ff,
                stop:1 #3a7bd5
            );
            border: none;
            border-radius: 12px;
            padding: 10px;
            font-size: 16px;
            font-weight: bold;
            color: white;
        }

        QPushButton#botonTarjeta:hover {
            background-color: qlineargradient(
                x1:0, y1:0, x2:1, y2:1,
                stop:0 #3a7bd5,
                stop:1 #00d2ff
            );
            border: 2px solid #00d2ff;
        }

        QPushButton#botonVolver {
            background-color: transparent;
            color: #00d2ff;
            font-size: 15px;
            border: 1px solid #00d2ff;
            padding: 10px 20px;
            border-radius: 12px;
        }

        QPushButton#botonVolver:hover {
            background-color: #1a1d2e;
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
        
    # def abrir_numeros_aleatorios(self):
    #     from Modulos.numeros_aleatorios.numeros_aleatorios import NumerosAleatorios 
    #     self.ventana = NumerosAleatorios()
    #     self.ventana.show()
    #     self.close()
        
    def abrir_MM(self):
        from Modulos.modelo_matematico.modelo_matematico import SimuladorSIR 
        self.ventana = SimuladorSIR()
        self.ventana.show()
        self.close()
        
    def abrir_acercade(self):
        from Modulos.acerca_de.acercade import AcercaDe
        self.ventana = AcercaDe()
        self.ventana.show()
        self.close()
