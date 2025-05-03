
from PyQt5.QtWidgets import *  # También importa todos los widgets

# Se importan componentes del núcleo de PyQt5, como señales personalizadas y alineación
from PyQt5.QtCore import Qt
# Se importa sympy, una librería para matemáticas simbólicas (por ejemplo, derivadas, integrales, ecuaciones)
import sympy as sp

# Se importa re, que es la librería de expresiones regulares para buscar o validar patrones en textos
import re


from Modulos.menu_general.menu_general import MenuGeneral




# Incluir módulos que permitan la derivación e integración de funciones
# matemáticas simbólicamente.
class CalculoSimbolico(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cálculo Simbólico")
        self.setStyleSheet("background-color: #0f111a; color: white; font-size: 16px;")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout(self)

        titulo = QLabel("🧮 Cálculo Simbólico")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 28px; font-weight: bold; color: #00d2ff;")
        layout.addWidget(titulo)

        self.input = QTextEdit()
        self.input.setPlaceholderText("Escribe una función como (3x^3)*sen(x)")
        self.input.setStyleSheet("background-color: #1e1e1e; border: 1px solid #00d2ff; border-radius: 10px;")
        self.input.setFixedHeight(100)
        layout.addWidget(self.input)

        fila = QHBoxLayout()
        self.opciones = QComboBox()
        self.opciones.addItems(["Derivar", "Integrar"])
        self.opciones.setStyleSheet("background-color: #1e1e1e; border: 1px solid #00d2ff;")
        fila.addWidget(self.opciones)

        self.variable_box = QTextEdit()
        self.variable_box.setPlaceholderText("Respecto a")
        self.variable_box.setFixedHeight(40)
        self.variable_box.setFixedWidth(120)
        self.variable_box.setStyleSheet("background-color: #1e1e1e; border: 1px solid #00d2ff;")
        fila.addWidget(self.variable_box)

        self.boton_calcular = QPushButton("Calcular")
        self.boton_calcular.setCursor(Qt.PointingHandCursor)
        self.boton_calcular.setStyleSheet("background-color: #00d2ff; font-weight: bold; border-radius: 10px; padding: 10px;")
        self.boton_calcular.clicked.connect(self.calcular)
        fila.addWidget(self.boton_calcular)
        
        # Botón Limpiar
        self.boton_limpiar = QPushButton("Limpiar")
        self.boton_limpiar.setCursor(Qt.PointingHandCursor)
        self.boton_limpiar.setStyleSheet("background-color: #ff6f61; font-weight: bold; border-radius: 10px; padding: 10px;")
        self.boton_limpiar.clicked.connect(self.limpiar_campos)
        fila.addWidget(self.boton_limpiar)

        # Botón Salir
        self.boton_salir = QPushButton("Salir")
        self.boton_salir.setCursor(Qt.PointingHandCursor)
        self.boton_salir.setStyleSheet("background-color: #ff4757; font-weight: bold; border-radius: 10px; padding: 10px;")
        self.boton_salir.clicked.connect(self.volver)
        fila.addWidget(self.boton_salir)
        layout.addLayout(fila)

        # Resultado
        self.resultado = QLabel("Resultado:")
        self.resultado.setWordWrap(True)
        self.resultado.setStyleSheet("background-color: #1e1e1e; border: 1px solid #00d2ff; padding: 12px; border-radius: 10px;")
        layout.addWidget(self.resultado)

        # Teclado
        self.teclado = self.crear_teclado()
        layout.addLayout(self.teclado)
        
    def limpiar_campos(self):
        self.input.clear()
        self.resultado.setText("Resultado:")
        
    def volver(self):
        self.menu = MenuGeneral()
        self.menu.show()
        self.close()

    def crear_teclado(self):
        teclado_widget = QWidget()
        teclado_layout = QGridLayout(teclado_widget)

        botones = [
            ('1', '1'), ('2', '2'), ('3', '3'), ('+', '+'),
            ('4', '4'), ('5', '5'), ('6', '6'), ('-', '-'),
            ('7', '7'), ('8', '8'), ('9', '9'), ('*', '*'),
            ('0', '0'), ('.', '.'), ('/', '/'), ('^', '**'),
            ('(', '('), (')', ')'), ('log', 'log('), ('exp', 'exp('),
            ('sen', 'sin('), ('cos', 'cos('), ('tan', 'tan('), ('√', 'sqrt('),
            ('π', 'pi'), ('x', 'x'), ('y', 'y'), ('z', 'z')
        ]

        for i, (texto, valor) in enumerate(botones):
            boton = QPushButton(texto)
            boton.setStyleSheet("""
                QPushButton {
                    background-color: #2c2f4a;
                    color: white;
                    font-weight: bold;
                    border-radius: 8px;
                    padding: 15px;
                }
                QPushButton:hover {
                    background-color: #3e4160;
                }
            """)
            boton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            boton.clicked.connect(self.crear_insertador(valor))
            teclado_layout.addWidget(boton, i // 4, i % 4)

        # Envolver en un scroll area para mejor comportamiento en ventanas pequeñas
        scroll_area = QScrollArea()
        scroll_area.setWidget(teclado_widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setStyleSheet("background-color: transparent;")

        # Contenedor de layout final
        teclado_contenedor = QVBoxLayout()
        teclado_contenedor.addWidget(scroll_area)

        return teclado_contenedor



    def crear_insertador(self, valor):
        def insertar():
            cursor = self.input.textCursor()
            cursor.insertText(valor)
        return insertar


    def preprocesar(self, texto):
        texto = texto.replace("^", "**")
        texto = texto.replace("sen", "sin")
        texto = texto.lower()

        funciones = ['sin', 'cos', 'tan', 'exp', 'log', 'sqrt']

        # Proteger funciones para evitar insertar * dentro de ellas
        for f in funciones:
            texto = re.sub(rf'\b{f}\(', f'__{f}__(' , texto)

        # Insertar * entre número y letra o paréntesis (3x → 3*x, 2(x+1) → 2*(x+1))
        texto = re.sub(r'(\d)([a-z\(])', r'\1*\2', texto)

        # Insertar * entre letra y número (x2 → x*2)
        texto = re.sub(r'([a-z])(\d)', r'\1*\2', texto)

        # Insertar * entre letra y paréntesis (x( → x*( )
        texto = re.sub(r'([a-z])\(', r'\1*(', texto)

        # Restaurar funciones protegidas
        for f in funciones:
            texto = texto.replace(f'__{f}__', f)

        return texto




    def calcular(self):
        entrada = self.input.toPlainText().strip().lower()
        variable_str = self.variable_box.toPlainText().strip().lower()

        if not entrada or not variable_str.isalpha():
            QMessageBox.warning(self, "Variable inválida", "Debes ingresar una expresión y una variable válida como x, y, z...")
            return

        try:
            entrada_proc = self.preprocesar(entrada)
            variable = sp.Symbol(variable_str)
            expresion = sp.sympify(entrada_proc)

            if self.opciones.currentText() == "Derivar":
                resultado = sp.diff(expresion, variable)
            else:
                resultado = sp.integrate(expresion, variable)
                resultado = sp.simplify(resultado)
                resultado = sp.expand(resultado)
                resultado = sp.nsimplify(resultado)
                resultado = sp.simplify(resultado)

            resultado_str = presentar_polinomio(resultado)
            if self.opciones.currentText() == "Integrar":
                resultado_str += " + C"

            self.resultado.setText(f"Resultado:\n{resultado_str}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo calcular. Asegúrate de que la expresión esté bien escrita.\n\n{str(e)}")

def presentar_polinomio(expr):
    expr = sp.expand(expr)
    return str(expr).replace("**", "^").replace("*", "")
