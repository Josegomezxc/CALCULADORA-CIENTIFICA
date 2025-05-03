from PyQt5.QtWidgets import *  # También importa todos los widgets

# Se importan componentes del núcleo de PyQt5, como señales personalizadas y alineación
from PyQt5.QtCore import Qt

# Se importa QPixmap para mostrar imágenes en la GUI
from PyQt5.QtGui import QPixmap

# Se importa sympy, una librería para matemáticas simbólicas (por ejemplo, derivadas, integrales, ecuaciones)
import sympy as sp

# Se importa re, que es la librería de expresiones regulares para buscar o validar patrones en textos
import re

from Modulos.menu_general.menu_general import MenuGeneral
from utils.helpers import resource_path


# Desarrollar funcionalidades para trabajar con polinomios, como suma,
# multiplicación, derivación, integración y evaluación.
class MenuPolinomios(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📈 Calculadora de Polinomios")  # Título de la ventana
        self.setGeometry(100, 100, 900, 600)  # Tamaño y posición de la ventana
        self.setStyleSheet(self.estilos())  # Aplicamos estilos visuales personalizados

        layout_principal = QVBoxLayout(self)  # Layout vertical principal
        layout_principal.setContentsMargins(40, 40, 40, 40)  # Márgenes alrededor
        layout_principal.setSpacing(30)  # Espaciado entre elementos

        # Título principal del menú
        titulo = QLabel("📈 Operaciones con Polinomios")
        titulo.setObjectName("titulo")  # Nombre del objeto para aplicar estilo
        layout_principal.addWidget(titulo)

        # Contenedor de las tarjetas de operaciones (en forma de grilla)
        grid = QGridLayout()
        grid.setSpacing(30)  # Espacio entre tarjetas
        grid.setAlignment(Qt.AlignCenter)  # Centra el contenido del grid

        # Lista de operaciones y sus funciones asociadas
        operaciones = [
            ("Sumar", self.abrir_suma),
            ("Multiplicar", self.abrir_multiplicacion),
            ("Derivadas", self.abrir_derivada),
            ("Integrales", self.abrir_integracion),
            ("Evaluar", self.abrir_evaluacion),
        ]

        row, col = 0, 0  # Posición inicial en el grid
        for texto, funcion in operaciones:
            tarjeta = self.crear_tarjeta(texto, funcion)  # Crear una tarjeta por operación
            grid.addWidget(tarjeta, row, col)  # Agregar la tarjeta al grid
            col += 1
            if col >= 3:  # Cambiar de fila cada 3 columnas
                row += 1
                col = 0

        layout_principal.addLayout(grid)  # Agregar el grid al layout principal

        # Botón para volver al menú principal
        boton_volver = QPushButton("Volver al menú principal")
        boton_volver.setObjectName("botonVolver")  # Estilo personalizado
        boton_volver.setCursor(Qt.PointingHandCursor)  # Cursor de mano al pasar
        boton_volver.setFixedWidth(240)  # Ancho fijo del botón
        boton_volver.clicked.connect(self.volver)  # Acción al hacer clic
        layout_principal.addWidget(boton_volver, alignment=Qt.AlignCenter)

    def crear_tarjeta(self, texto, funcion):
        tarjeta = QFrame()  # Contenedor tipo tarjeta
        tarjeta.setObjectName("tarjeta")  # Para aplicar estilos CSS
        tarjeta.setFixedSize(240, 160)  # Tamaño fijo de cada tarjeta

        layout = QVBoxLayout(tarjeta)  # Layout vertical dentro de la tarjeta
        layout.setContentsMargins(15, 15, 15, 15)  # Márgenes internos
        layout.setAlignment(Qt.AlignCenter)  # Centra el contenido

        # Imagen decorativa de la operación
        imagen_label = QLabel()
        ruta_imagen = resource_path(f"images/{texto.lower()}.png")  # Ruta de la imagen
        pixmap = QPixmap(ruta_imagen).scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        imagen_label.setPixmap(pixmap)
        imagen_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(imagen_label)

        # Botón dentro de la tarjeta
        boton = QPushButton(texto)
        boton.setObjectName("botonTarjeta")  # Estilo visual del botón
        boton.setCursor(Qt.PointingHandCursor)  # Cursor al pasar
        boton.setFixedSize(180, 60)  # Tamaño del botón
        boton.clicked.connect(funcion)  # Acción al hacer clic
        layout.addWidget(boton)

        return tarjeta  # Devuelve la tarjeta creada

    def estilos(self):
        # Estilos CSS personalizados para la interfaz
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

    # Las siguientes funciones abren la calculadora con la operación correspondiente
    def abrir_suma(self):
        self.abrir_operacion("Sumar")

    def abrir_multiplicacion(self):
        self.abrir_operacion("Multiplicar")

    def abrir_derivada(self):
        self.abrir_operacion("Derivadas")

    def abrir_integracion(self):
        self.abrir_operacion("Integrales")

    def abrir_evaluacion(self):
        self.abrir_operacion("Evaluar")

    # Función que abre la ventana correspondiente a la operación seleccionada
    def abrir_operacion(self, operacion):
        self.ventana = CalculadoraPolinomios(operacion)
        self.ventana.show()
        self.close()

    # Función que vuelve al menú principal
    def volver(self):
        self.menu = MenuGeneral()
        self.menu.show()
        self.close()

        
class CalculadoraPolinomios(QWidget):
    def __init__(self, operacion):
        super().__init__()
        self.operacion = operacion  # Se guarda la operación que el usuario seleccionó
        self.setWindowTitle(f"Operación: {self.operacion}")  # Se configura el título de la ventana
        self.setGeometry(100, 100, 900, 600)  # Tamaño y posición de la ventana

        # Layout principal vertical
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Mostrar qué operación fue seleccionada
        self.layout.addWidget(QLabel(f"Operación seleccionada: {self.operacion}"))

        # Campo de entrada para el Polinomio A
        self.polynomial_a_label = QLabel("Polinomio A:")
        self.polynomial_a_input = QLineEdit()
        self.polynomial_a_input.setPlaceholderText("Ejemplo: 3x^2 + 2x + 1")
        self.layout.addWidget(self.polynomial_a_label)
        self.layout.addWidget(self.polynomial_a_input)

        # Campo de entrada para el Polinomio B
        self.polynomial_b_label = QLabel("Polinomio B:")
        self.polynomial_b_input = QLineEdit()
        self.polynomial_b_input.setPlaceholderText("Ejemplo: 3x^2 + 2x + 1 ")

        # Mostrar campo B solo si la operación lo necesita
        if self.operacion in ["Sumar", "Multiplicar"]:
            self.layout.addWidget(self.polynomial_b_label)
            self.layout.addWidget(self.polynomial_b_input)

        # Área para mostrar el resultado (solo lectura)
        self.resultado = QTextEdit()
        self.resultado.setReadOnly(True)
        self.resultado.setStyleSheet("""
            font-size: 20px;
            color: #00d2ff;
            background-color: #1a1d2e;
            border: 1px solid #00d2ff;
            border-radius: 10px;
            padding: 10px;
        """)
        self.layout.addWidget(QLabel("Resultado:"))
        self.layout.addWidget(self.resultado)

        # Botones: Calcular, Limpiar, Volver
        botones_layout = QHBoxLayout()
        self.boton_calcular = QPushButton("Calcular")
        self.boton_calcular.clicked.connect(self.calcular)
        self.boton_limpiar = QPushButton("Limpiar")
        self.boton_limpiar.clicked.connect(self.limpiar_campos)
        self.boton_volver = QPushButton("Volver al menú")
        self.boton_volver.clicked.connect(self.volver_al_menu)

        botones_layout.addWidget(self.boton_calcular)
        botones_layout.addWidget(self.boton_limpiar)
        botones_layout.addWidget(self.boton_volver)
        self.layout.addLayout(botones_layout)

    def calcular(self):
        # Obtener los textos de entrada y convertirlos a minúsculas
        polinomio_a = self.polynomial_a_input.text().strip().lower()
        polinomio_b = self.polynomial_b_input.text().strip().lower()

        # Si las entradas están vacías, se rellenan con "0"
        if not polinomio_a:
            polinomio_a = "0"
            self.polynomial_a_input.setText("0")
        if not polinomio_b:
            polinomio_b = "0"
            self.polynomial_b_input.setText("0")

        # Función para formatear el texto ingresado en un formato que sympy entienda
        def formatear_polinomio(entrada):
            entrada = entrada.replace('^', '**')  # Cambia potencias a formato de Python
            entrada = entrada.lower()
            entrada = re.sub(r'([a-z])(?=[a-z])', r'\1*', entrada)
            entrada = re.sub(r'(\d)([a-z])', r'\1*\2', entrada)
            entrada = re.sub(r'([a-z])(\d)', r'\1*\2', entrada)
            entrada = re.sub(r'([a-z])\(', r'\1*(', entrada)
            return entrada

        # Función para mostrar el resultado en un formato más limpio
        def presentar_polinomio(expr):
            texto = str(expr)
            texto = texto.replace('**', '^')
            texto = re.sub(r'\b1\*', '', texto)
            texto = re.sub(r'(\d)\*([a-z])', r'\1\2', texto)
            texto = texto.replace('*', '')
            return texto

        # Se crean variables simbólicas para todas las letras del abecedario
        letras = 'abcdefghijklmnopqrstuvwxyz'
        variables = sp.symbols(' '.join(letras))
        variables_dict = dict(zip(letras, variables))

        try:
            # Formatear entradas
            entrada_a = formatear_polinomio(polinomio_a if polinomio_a else "0")
            entrada_b = formatear_polinomio(polinomio_b if polinomio_b else "0")

            # Operación: Suma
            if self.operacion == "Sumar":   
                poly_a = sp.Poly(sp.sympify(entrada_a, locals=variables_dict)).as_expr()
                poly_b = sp.Poly(sp.sympify(entrada_b, locals=variables_dict)).as_expr()
                resultado_expr = sp.simplify(poly_a + poly_b)
                resultado_str = presentar_polinomio(resultado_expr)
                self.resultado.setText(f"Resultado:\n{resultado_str}")

            # Operación: Multiplicación
            elif self.operacion == "Multiplicar":
                poly_a = sp.Poly(sp.sympify(entrada_a, locals=variables_dict)).as_expr()
                poly_b = sp.Poly(sp.sympify(entrada_b, locals=variables_dict)).as_expr()
                resultado_expr = sp.simplify(poly_a * poly_b)
                resultado_str = presentar_polinomio(resultado_expr)
                self.resultado.setText(f"Resultado:\n{resultado_str}")

            # Operación: Derivada
            elif self.operacion == "Derivadas":
                var_str, ok = QInputDialog.getText(self, "Variable", "¿Respecto a qué variable quieres derivar? (por ejemplo: x, y, z)")
                if not ok or not var_str.isalpha():
                    QMessageBox.warning(self, "Variable inválida", "Debes ingresar una variable válida (una letra como x, y, z).")
                    return

                variable = variables_dict.get(var_str.strip().lower())
                if variable is None:
                    QMessageBox.warning(self, "Variable inválida", "Variable no reconocida.")
                    return

                poly_a = sp.sympify(entrada_a, locals=variables_dict)
                resultado_expr = sp.diff(poly_a, variable)
                resultado_str = presentar_polinomio(resultado_expr)
                self.resultado.setText(f"Resultado:\n{resultado_str}")

            # Operación: Integral
            elif self.operacion == "Integrales":
                var_str, ok = QInputDialog.getText(self, "Variable", "¿Respecto a qué variable quieres integrar? (por ejemplo: x, y, z)")
                if not ok or not var_str.isalpha():
                    QMessageBox.warning(self, "Variable inválida", "Debes ingresar una variable válida (una letra como x, y, z).")
                    return

                variable = variables_dict.get(var_str.strip().lower())
                if variable is None:
                    QMessageBox.warning(self, "Variable inválida", "Variable no reconocida.")
                    return

                poly_a = sp.sympify(entrada_a, locals=variables_dict)
                resultado_expr = sp.integrate(poly_a, variable)
                resultado_str = presentar_polinomio(resultado_expr) + " + C"  # Se agrega + C al final por ser una integral indefinida
                self.resultado.setText(f"Resultado:\n{resultado_str}")

            # Operación: Evaluación
            elif self.operacion == "Evaluar":
                valor, ok = QInputDialog.getDouble(self, "Evaluar", "¿En qué valor deseas evaluar el polinomio?")
                if ok:
                    x = variables_dict['x']
                    poly_a = sp.sympify(entrada_a, locals=variables_dict)
                    resultado_eval = poly_a.subs(x, valor)
                    resultado_str = presentar_polinomio(resultado_eval)
                    self.resultado.setText(f"Resultado:\n{resultado_str}")
                else:
                    self.resultado.setText("Evaluación cancelada.")

        except Exception as e:
            # Si ocurre un error en el proceso, se muestra un mensaje de advertencia
            self.resultado.setText("Error en el procesamiento del polinomio.\nVerifica la sintaxis.\nEjemplo: 3x^2 + 2x + 1")

    # Limpia todos los campos de entrada y resultado
    def limpiar_campos(self):
        self.polynomial_a_input.clear()
        self.polynomial_b_input.clear()
        self.resultado.clear()

    # Regresa al menú anterior
    def volver_al_menu(self):
        self.menu = MenuPolinomios()
        self.menu.show()
        self.close()

