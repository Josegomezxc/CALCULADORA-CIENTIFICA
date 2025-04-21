import numpy as np
import matplotlib.pyplot as plt
import re
from numpy import sin, cos, tan, exp, log, sqrt, pi, e

def procesar_funcion(expr):
    expr = expr.replace(" ", "")        # Eliminar espacios
    expr = expr.replace("^", "**")      # Reemplazar potencias

    # Asegurar multiplicación implícita
    expr = re.sub(r"(\d)([a-zA-Z\(])", r"\1*\2", expr)     # 2x o 2sin -> 2*x o 2*sin
    expr = re.sub(r"(\))([a-zA-Z\d\(])", r"\1*\2", expr)   # )x o )2 -> )*x o )*2
    expr = re.sub(r"([a-zA-Z])(\()", r"\1*\2", expr)       # x(2x) -> x*(2x)
    expr = re.sub(r"([a-zA-Z])([a-zA-Z])", r"\1*\2", expr) # xsin -> x*sin

    # Convertir ln(x) a log(x)
    expr = expr.replace("ln", "log")

    # Balancear paréntesis
    abrir = expr.count("(")
    cerrar = expr.count(")")
    if abrir > cerrar:
        expr += ")" * (abrir - cerrar)

    return expr

def graficar_funcion_personalizada():
    funcion_usuario = input("Ingresa la función en x que deseas graficar (ej. 2xsin(2x)): ")

    x = np.linspace(0.1, 10, 300)
    expr = procesar_funcion(funcion_usuario)

    try:
        y = eval(expr, {
            "x": x, "sin": sin, "cos": cos, "tan": tan,
            "log": log, "exp": exp, "sqrt": sqrt,
            "pi": pi, "e": e, "np": np
        })

        plt.figure(figsize=(6, 4))
        plt.plot(x, y, color="blue")
        plt.title(f"Gráfico de: y = {funcion_usuario}")
        plt.grid(True)
        plt.xlabel("x")
        plt.ylabel("y")
        plt.show()

    except Exception as error:
        print(f"\n❌ Error al graficar la función:\n{error}\n")
        print("Revisa la sintaxis de la función que ingresaste.")

# Ejecutar
graficar_funcion_personalizada()
