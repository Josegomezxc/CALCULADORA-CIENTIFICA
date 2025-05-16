from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox,
    QTextEdit, QGridLayout, QScrollArea, QFrame, QSizePolicy, QLineEdit, QMessageBox
)
from PyQt5.QtCore import Qt
import sympy as sp
import re
from Modulos.menu_general.menu_general import MenuGeneral

class CalculoSimbolico(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cálculo Simbólico")
        self.setStyleSheet("background-color: #0f111a; color: white; font-size: 16px;")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout(self)

        # Título
        titulo = QLabel("🧮 Cálculo Simbólico")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 28px; font-weight: bold; color: #00d2ff;")
        layout.addWidget(titulo)

        # Entrada de la función
        self.input = QTextEdit()
        self.input.setPlaceholderText("Escribe una función como (3x^3)*sin(x)")
        self.input.setStyleSheet("background-color: #1e1e1e; border: 1px solid #00d2ff; border-radius: 10px;")
        self.input.setFixedHeight(100)
        layout.addWidget(self.input)

        # Parámetros
        params_layout = QGridLayout()

        # Selección de operación
        self.opciones = QComboBox()
        self.opciones.addItems(["Derivar", "Integrar Indefinida", "Integrar Definida", "Integrar por Partes"])
        self.opciones.setStyleSheet("background-color: #1e1e1e; border: 1px solid #00d2ff; border-radius: 6px; padding: 4px;")
        self.opciones.currentIndexChanged.connect(self.toggle_limites)
        params_layout.addWidget(QLabel("Operación:"), 0, 0)
        params_layout.addWidget(self.opciones, 0, 1)

        # Variable
        self.variable_box = QTextEdit()
        self.variable_box.setPlaceholderText("Respecto a (ej. x)")
        self.variable_box.setFixedHeight(40)
        self.variable_box.setFixedWidth(120)
        self.variable_box.setStyleSheet("background-color: #1e1e1e; border: 1px solid #00d2ff; border-radius: 6px;")
        params_layout.addWidget(QLabel("Variable:"), 1, 0)
        params_layout.addWidget(self.variable_box, 1, 1)

        # Límites para integración definida
        self.limite_inf = QLineEdit()
        self.limite_inf.setPlaceholderText("Límite inferior")
        self.limite_inf.setFixedWidth(120)
        self.limite_inf.setStyleSheet("background-color: #1e1e1e; border: 1px solid #00d2ff; border-radius: 6px;")
        self.limite_inf.setVisible(False)
        params_layout.addWidget(QLabel("Límite inferior:"), 2, 0)
        params_layout.addWidget(self.limite_inf, 2, 1)

        self.limite_sup = QLineEdit()
        self.limite_sup.setPlaceholderText("Límite superior")
        self.limite_sup.setFixedWidth(120)
        self.limite_sup.setStyleSheet("background-color: #1e1e1e; border: 1px solid #00d2ff; border-radius: 6px;")
        self.limite_sup.setVisible(False)
        params_layout.addWidget(QLabel("Límite superior:"), 3, 0)
        params_layout.addWidget(self.limite_sup, 3, 1)

        layout.addLayout(params_layout)

        # Botones
        button_layout = QHBoxLayout()

        self.boton_calcular = QPushButton("Calcular")
        self.boton_calcular.setCursor(Qt.PointingHandCursor)
        self.boton_calcular.setStyleSheet("background-color: #00d2ff; font-weight: bold; border-radius: 10px; padding: 10px;")
        self.boton_calcular.clicked.connect(self.calcular)
        button_layout.addWidget(self.boton_calcular)

        self.boton_limpiar = QPushButton("Limpiar")
        self.boton_limpiar.setCursor(Qt.PointingHandCursor)
        self.boton_limpiar.setStyleSheet("background-color: #ff6f61; font-weight: bold; border-radius: 10px; padding: 10px;")
        self.boton_limpiar.clicked.connect(self.limpiar_campos)
        button_layout.addWidget(self.boton_limpiar)

        self.boton_salir = QPushButton("Volver")
        self.boton_salir.setCursor(Qt.PointingHandCursor)
        self.boton_salir.setStyleSheet("background-color: #ff4757; font-weight: bold; border-radius: 10px; padding: 10px;")
        self.boton_salir.clicked.connect(self.volver)
        button_layout.addWidget(self.boton_salir)

        layout.addLayout(button_layout)

        # Resultado
        self.resultado = QLabel("Resultado:")
        self.resultado.setWordWrap(True)
        self.resultado.setStyleSheet("background-color: #1e1e1e; border: 1px solid #00d2ff; padding: 12px; border-radius: 10px;")
        layout.addWidget(self.resultado)

        # Teclado
        self.teclado = self.crear_teclado()
        layout.addLayout(self.teclado)

    def toggle_limites(self):
        es_definida = self.opciones.currentText() == "Integrar Definida"
        self.limite_inf.setVisible(es_definida)
        self.limite_sup.setVisible(es_definida)

    def limpiar_campos(self):
        self.input.clear()
        self.variable_box.clear()
        self.limite_inf.clear()
        self.limite_sup.clear()
        self.resultado.setText("Resultado:")
        self.opciones.setCurrentIndex(0)
        self.toggle_limites()

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
            ('sin', 'sin('), ('cos', 'cos('), ('tan', 'tan('), ('√', 'sqrt('),
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

        scroll_area = QScrollArea()
        scroll_area.setWidget(teclado_widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setStyleSheet("background-color: transparent;")

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

        for f in funciones:
            texto = re.sub(rf'\b{f}\(', f'__{f}__(' , texto)

        texto = re.sub(r'(\d)([a-z\(])', r'\1*\2', texto)
        texto = re.sub(r'([a-z])(\d)', r'\1*\2', texto)
        texto = re.sub(r'([a-z])\(', r'\1*(', texto)

        for f in funciones:
            texto = texto.replace(f'__{f}__', f)

        return texto

    def integracion_por_partes(self, expr, variable):
        # Simplificar la expresión inicial
        expr = sp.simplify(expr)
        # Verificar si la expresión es un producto usando factores
        factors = expr.as_ordered_factors()
        if len(factors) >= 2:
            # Intentar con cada factor como u, priorizando según LIATE (aproximado)
            for u in factors:
                dv = expr / u
                if dv.has(variable):
                    try:
                        # Simplificar dv antes de integrar
                        dv = sp.simplify(dv)
                        v = sp.integrate(dv, variable)
                        v = sp.simplify(v)
                        du = sp.diff(u, variable)
                        du = sp.simplify(du)
                        # Calcular la integral por partes
                        result = u * v - sp.integrate(v * du, variable)
                        # Simplificar el resultado
                        result = sp.simplify(sp.expand(sp.nsimplify(result)))
                        pasos = [
                            f"Elegimos u = {presentar_polinomio(u)}, dv = {presentar_polinomio(dv)} dx",
                            f"Entonces, du = {presentar_polinomio(du)} dx, v = {presentar_polinomio(v)}",
                            f"Aplicamos: ∫u dv = uv - ∫v du = {presentar_polinomio(u * v)} - ∫{presentar_polinomio(v * du)} dx",
                            f"Resultado: {presentar_polinomio(result)}"
                        ]
                        return result, pasos
                    except Exception:
                        continue
        # Si no es un producto claro o falla, integrar directamente
        result = sp.integrate(expr, variable)
        result = sp.simplify(sp.expand(sp.nsimplify(result)))
        return result, ["La expresión no permitió una integración por partes clara, se integró directamente."]

    def calcular(self):
        entrada = self.input.toPlainText().strip().lower()
        variable_str = self.variable_box.toPlainText().strip().lower()
        operacion = self.opciones.currentText()

        if not entrada or not variable_str.isalpha():
            QMessageBox.warning(self, "Entrada inválida", "Debes ingresar una expresión y una variable válida (ej. x, y, z).")
            return

        try:
            entrada_proc = self.preprocesar(entrada)
            variable = sp.Symbol(variable_str)
            expresion = sp.sympify(entrada_proc)

            if operacion == "Derivar":
                resultado = sp.diff(expresion, variable)
                resultado_str = presentar_polinomio(resultado)
                self.resultado.setText(f"Derivada:\n{resultado_str}")

            elif operacion == "Integrar Indefinida":
                resultado = sp.integrate(expresion, variable)
                resultado = sp.simplify(sp.expand(sp.nsimplify(resultado)))
                resultado_str = presentar_polinomio(resultado) + " + C"
                self.resultado.setText(f"Integral indefinida:\n{resultado_str}")

            elif operacion == "Integrar Definida":
                lim_inf = self.limite_inf.text().strip()
                lim_sup = self.limite_sup.text().strip()
                if not lim_inf or not lim_sup:
                    QMessageBox.warning(self, "Límites inválidos", "Debes ingresar límites inferior y superior.")
                    return
                try:
                    lim_inf_val = sp.sympify(lim_inf)
                    lim_sup_val = sp.sympify(lim_sup)
                    resultado = sp.integrate(expresion, (variable, lim_inf_val, lim_sup_val))
                    resultado = sp.simplify(sp.expand(sp.nsimplify(resultado)))
                    resultado_str = presentar_polinomio(resultado)
                    self.resultado.setText(f"Integral definida de {lim_inf} a {lim_sup}:\n{resultado_str}")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"No se pudo evaluar los límites: {str(e)}")
                    return

            elif operacion == "Integrar por Partes":
                resultado, pasos = self.integracion_por_partes(expresion, variable)
                resultado = sp.simplify(sp.expand(sp.nsimplify(resultado)))
                resultado_str = presentar_polinomio(resultado) + " + C"
                pasos_str = "\n".join(pasos)
                self.resultado.setText(f"Integral por partes:\nPasos:\n{pasos_str}\n\nResultado:\n{resultado_str}")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo calcular. Asegúrate de que la expresión esté bien escrita.\n\n{str(e)}")

def presentar_polinomio(expr):
    # Simplificar la expresión para eliminar Piecewise y términos como log(e)
    expr = sp.simplify(sp.expand(sp.nsimplify(expr)))
    # Convertir a string y limpiar la notación
    result = str(expr).replace("**", "^").replace("*", "")
    # Reemplazar términos específicos
    result = result.replace("log(e)", "1")
    # Manejar Piecewise manualmente (tomar la rama principal si es simple)
    if "Piecewise" in result:
        try:
            # Extraer la primera rama de Piecewise si es aplicable
            expr = expr.subs(sp.Symbol('e'), sp.E)  # Asegurar que e es la constante
            expr = sp.simplify(expr)
            result = str(expr).replace("**", "^").replace("*", "").replace("log(e)", "1")
        except:
            result = str(expr).replace("**", "^").replace("*", "")
    return result

