
# Importa el módulo math para operaciones matemáticas básicas como raíces, potencias, etc.
import math

from PyQt5.QtWidgets import *  # También importa todos los widgets

# Se importan componentes del núcleo de PyQt5, como señales personalizadas y alineación
from PyQt5.QtCore import Qt

# Se importa QPixmap para mostrar imágenes en la GUI
from PyQt5.QtGui import QPixmap

# Se importa re, que es la librería de expresiones regulares para buscar o validar patrones en textos
import re

from Modulos.menu_general.menu_general import MenuGeneral
from utils.helpers import resource_path


class MenuVectores(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📐 Calculadora de Vectores")  # Título de la ventana
        self.setGeometry(100, 100, 900, 600)  # Posición y tamaño de la ventana
        self.setStyleSheet(self.estilos())  # Se aplican estilos personalizados

        layout_principal = QVBoxLayout(self)  # Layout vertical principal
        layout_principal.setContentsMargins(40, 40, 40, 40)  # Márgenes exteriores
        layout_principal.setSpacing(30)  # Espaciado entre elementos del layout

        # Título principal de la ventana
        titulo = QLabel("📐 Operaciones con Vectores")
        titulo.setObjectName("titulo")  # ID para aplicar estilo
        layout_principal.addWidget(titulo)

        # Grid que contiene las tarjetas de operaciones
        grid = QGridLayout()
        grid.setSpacing(30)  # Espacio entre tarjetas
        grid.setAlignment(Qt.AlignCenter)  # Centrado del contenido del grid

        # Lista de operaciones disponibles y su función correspondiente
        operaciones = [
            ("Sumar", self.abrir_suma),
            ("Restar", self.abrir_resta),
            ("Producto Punto", self.abrir_producto_punto),
            ("Magnitud", self.abrir_magnitud),
            ("Producto Cruz", self.abrir_producto_cruz),
        ]

        row, col = 0, 0  # Posición inicial del grid
        for texto, funcion in operaciones:
            tarjeta = self.crear_tarjeta(texto, funcion)  # Crear tarjeta para cada operación
            grid.addWidget(tarjeta, row, col)  # Agregar tarjeta al grid
            col += 1
            if col >= 3:  # Cambiar a la siguiente fila cada 3 columnas
                row += 1
                col = 0

        layout_principal.addLayout(grid)  # Añadir el grid al layout principal

        # Botón para volver al menú principal
        boton_volver = QPushButton("Volver al menú principal")
        boton_volver.setObjectName("botonVolver")  # Estilo personalizado
        boton_volver.setCursor(Qt.PointingHandCursor)  # Cursor en forma de mano
        boton_volver.setFixedWidth(240)  # Ancho fijo del botón
        boton_volver.clicked.connect(self.volver)  # Acción al hacer clic
        layout_principal.addWidget(boton_volver, alignment=Qt.AlignCenter)

    def crear_tarjeta(self, texto, funcion):
        tarjeta = QFrame()  # Tarjeta contenedora de imagen + botón
        tarjeta.setObjectName("tarjeta")  # ID para aplicar estilo
        tarjeta.setFixedSize(240, 160)  # Tamaño fijo

        layout = QVBoxLayout(tarjeta)  # Layout vertical dentro de la tarjeta
        layout.setContentsMargins(15, 15, 15, 15)  # Márgenes internos
        layout.setAlignment(Qt.AlignCenter)  # Centrado del contenido

        # Imagen representativa de la operación
        imagen_label = QLabel()
        ruta_imagen = resource_path(f"images/{texto.lower().replace(' ','_')}.png")  # Ruta a la imagen
        pixmap = QPixmap(ruta_imagen).scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        imagen_label.setPixmap(pixmap)
        imagen_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(imagen_label)

        # Botón que representa la operación
        boton = QPushButton(texto)
        boton.setObjectName("botonTarjeta")  # ID para aplicar estilo
        boton.setCursor(Qt.PointingHandCursor)  # Cursor en forma de mano
        boton.setFixedSize(180, 60)  # Tamaño fijo
        boton.clicked.connect(funcion)  # Acción al hacer clic
        layout.addWidget(boton)

        return tarjeta  # Devolver la tarjeta creada

    def estilos(self):
        # Estilos personalizados de la interfaz (colores, bordes, fuentes, etc.)
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

    # Métodos que abren la calculadora para cada operación
    def abrir_suma(self):
        self.abrir_operacion("Sumar")

    def abrir_resta(self):
        self.abrir_operacion("Restar")

    def abrir_producto_punto(self):
        self.abrir_operacion("Producto Punto")

    def abrir_magnitud(self):
        self.abrir_operacion("Magnitud")

    def abrir_producto_cruz(self):
        self.abrir_operacion("Producto Cruz")

    # Método genérico que abre la ventana de cálculo según la operación
    def abrir_operacion(self, operacion):
        self.ventana = CalculadoraVectores(operacion)
        self.ventana.show()
        self.close()

    # Método que regresa al menú principal
    def volver(self):
        self.menu = MenuGeneral()
        self.menu.show()
        self.close()


class CalculadoraVectores(QWidget):
    def __init__(self, operacion):
        super().__init__()
        self.operacion = operacion  # Guarda la operación seleccionada (Suma, Resta, etc.)
        self.setWindowTitle(f"📐 {operacion} de Vectores")  # Título de la ventana
        self.setGeometry(100, 100, 800, 500)  # Tamaño y posición inicial de la ventana
        self.setStyleSheet("background-color: #0f111a; color: white; font-size: 16px;")  # Estilos generales

        layout_principal = QVBoxLayout(self)  # Layout principal vertical
        layout_principal.setContentsMargins(40, 40, 40, 40)  # Márgenes
        layout_principal.setSpacing(20)  # Espaciado entre elementos

        # Título principal
        titulo = QLabel(f"📐 {operacion} de Vectores")
        titulo.setStyleSheet("font-size: 26px; font-weight: bold; color: #00d2ff;")
        titulo.setAlignment(Qt.AlignCenter)
        layout_principal.addWidget(titulo)
        
        # Etiqueta y campo de entrada para el primer vector
        label_vector1 = QLabel("Vector 1:")
        label_vector1.setStyleSheet("font-weight: bold; color: #00d2ff; font-size: 16px;")
        layout_principal.addWidget(label_vector1)

        self.entrada1 = QLineEdit()
        self.entrada1.setPlaceholderText("Ej: 1, 2, 3")  # Texto de ejemplo
        self.entrada1.setStyleSheet("padding: 10px; border-radius: 10px; background-color: #1a1d2e;")
        layout_principal.addWidget(self.entrada1)

        # Si la operación no es Magnitud, también se pide un segundo vector
        if operacion != "Magnitud":
            label_vector2 = QLabel("Vector 2:")
            label_vector2.setStyleSheet("font-weight: bold; color: #00d2ff; font-size: 16px;")
            layout_principal.addWidget(label_vector2)

            self.entrada2 = QLineEdit()
            self.entrada2.setPlaceholderText("Ej: 4, 5, 6")
            self.entrada2.setStyleSheet("padding: 10px; border-radius: 10px; background-color: #1a1d2e;")
            layout_principal.addWidget(self.entrada2)

        # Botón para calcular el resultado
        self.boton_calcular = QPushButton("Calcular")
        self.boton_calcular.setStyleSheet("""
            QPushButton {
                background-color: #00d2ff;
                border: none;
                border-radius: 10px;
                padding: 10px;
                font-weight: bold;
                color: black;
            }
            QPushButton:hover {
                background-color: #3a7bd5;
                color: white;
            }
        """)
        self.boton_calcular.clicked.connect(self.calcular)
        layout_principal.addWidget(self.boton_calcular)

        # Área donde se muestra el resultado
        self.resultado = QLabel("")
        self.resultado.setAlignment(Qt.AlignCenter)
        self.resultado.setWordWrap(True)  # Permite que el texto se ajuste al ancho
        self.resultado.setStyleSheet("font-size: 18px; color: #f1f1f1; padding-top: 20px;")
        layout_principal.addWidget(self.resultado)

        # Botón para volver al menú de vectores
        boton_volver = QPushButton("Volver")
        boton_volver.setStyleSheet("""
            QPushButton {
                color: #00d2ff;
                border: 1px solid #00d2ff;
                border-radius: 10px;
                padding: 8px;
                background-color: transparent;
            }
            QPushButton:hover {
                background-color: #1a1d2e;
            }
        """)
        boton_volver.clicked.connect(self.volver)
        layout_principal.addWidget(boton_volver, alignment=Qt.AlignCenter)
        
    def limpiar_entrada(self, texto):
        # Limpia la entrada del usuario eliminando espacios y comas innecesarias
        texto = re.sub(r'[,\s]+', ',', texto.strip())  # Reemplaza espacios o comas múltiples por una sola coma
        texto = re.sub(r'-+', '-', texto)  # Reemplaza múltiples signos negativos por uno solo
        texto = texto.strip(',')  # Quita comas al principio o final
        return texto

    def calcular(self):
        try:
            # Limpieza de los textos ingresados
            texto1 = self.limpiar_entrada(self.entrada1.text())
            texto2 = self.limpiar_entrada(self.entrada2.text()) if self.operacion != "Magnitud" else ""

            # Convertir los textos a listas de números flotantes
            vector1 = list(map(float, texto1.split(','))) if texto1 else []
            vector2 = list(map(float, texto2.split(','))) if texto2 else []

            # Validar si hay entradas vacías
            if not vector1 and not vector2 and self.operacion != "Magnitud":
                self.resultado.setText("Por favor, ingresa al menos un vector.")
                return
            if not vector1 and self.operacion == "Magnitud":
                self.resultado.setText("Por favor, ingresa un vector.")
                return

            # Rellenar con ceros si uno de los vectores está vacío
            if self.operacion != "Magnitud":
                if not vector1:
                    vector1 = [0.0] * len(vector2)
                    self.entrada1.setText(', '.join(map(str, vector1)))
                elif not vector2:
                    vector2 = [0.0] * len(vector1)
                    self.entrada2.setText(', '.join(map(str, vector2)))

                # Verificar que ambos vectores tengan la misma dimensión
                if self.operacion in ["Sumar", "Restar", "Producto Punto", "Producto Cruz"] and len(vector1) != len(vector2):
                    self.resultado.setText("❌ Los vectores deben tener la misma dimensión.")
                    return

            # Realizar la operación correspondiente
            if self.operacion == "Sumar":
                resultado = [a + b for a, b in zip(vector1, vector2)]
            elif self.operacion == "Restar":
                resultado = [a - b for a, b in zip(vector1, vector2)]
            elif self.operacion == "Producto Punto":
                resultado = sum(a * b for a, b in zip(vector1, vector2))
            elif self.operacion == "Magnitud":
                resultado = round(math.sqrt(sum(a ** 2 for a in vector1)), 4)  # Magnitud (norma del vector)
            elif self.operacion == "Producto Cruz":
                if len(vector1) != 3 or len(vector2) != 3:
                    self.resultado.setText("❌ El producto cruz solo se define en R³.")
                    return
                # Fórmula del producto cruzado
                a1, a2, a3 = vector1
                b1, b2, b3 = vector2
                resultado = [
                    a2 * b3 - a3 * b2,
                    a3 * b1 - a1 * b3,
                    a1 * b2 - a2 * b1
                ]
            else:
                resultado = "❌ Operación no reconocida."  # Si no coincide con ninguna operación válida

            # Mostrar el resultado
            self.resultado.setText(f"✅ Resultado: {resultado}")

        except ValueError:
            # Error al convertir texto a números
            self.resultado.setText("❌ Entrada inválida. Solo se permiten números separados por comas (ej: 1, 2, 3).")

    def volver(self):
        # Volver al menú de vectores
        self.menu_vectores = MenuVectores()
        self.menu_vectores.show()
        self.close()
