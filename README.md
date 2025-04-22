
# Calculadora Científica con Interfaz Gráfica

## 📘 Introducción al Programa

Este programa es una **calculadora científica con interfaz gráfica desarrollada en Python**, creada como parte de una actividad de la asignatura **Modelos Matemáticos y Simulación**.

Está diseñada para facilitar la resolución de ejercicios matemáticos, abarcando conceptos como operaciones con matrices, polinomios, vectores, funciones matemáticas, y visualización gráfica en 2D y 3D.

La calculadora permite realizar cálculos tanto **numéricos como simbólicos** mediante una interfaz intuitiva y estructurada por módulos. Cada módulo ayuda a reforzar habilidades de modelación matemática, simulación y programación.

**Autor**: Gómez Molina José Andrés  
**Carrera**: Ingeniería en Software  
**Semestre**: 6to  
**Año académico**: 2025  
**Materia**: Modelos Matemáticos y Simulación  
**Profesor**: Ing. Morales Torres Isidro Fabricio  

---

## 🛠 Instalación

### Código necesario para instalar todos los módulos requeridos:

```bash
pip install pyqt5 matplotlib numpy sympy
```

---

### Instalar PyInstaller para poder crear el archivo ejecutable `.exe`:

```bash
pip install pyinstaller
```

---

### Crear el ejecutable:

Una vez instalado PyInstaller, use el siguiente comando para generar el `.exe`:

```bash
pyinstaller --noconfirm --windowed --onefile --add-data "images;images" --add-data "styles.css;." app.py
```

Esto generará un ejecutable llamado `app.exe` dentro de la carpeta `dist/`.

---

## 🚀 Instrucciones para ejecutar

1. Ubique el icono de la aplicación llamado **“app.exe”** en su computadora.
2. Haga **doble clic** sobre el icono con el botón izquierdo del mouse.
3. El programa se abrirá y podrá comenzar a usarlo.

---

## 🧩 Capturas de pantalla de cada módulo (descripción visual)

### 🔹 Módulo Principal

Al ejecutar el programa, se muestra el **menú principal** con varias opciones disponibles para el usuario.

---

### 🔹 Módulo de Calculadora de Matrices

Opciones disponibles:

- Sumar matrices  
- Restar matrices  
- Multiplicar matrices  
- Inversa de una matriz  
- Determinante de una matriz  
- Solución de Sistemas Lineales

---

### 🔹 Módulo de Polinomios

Opciones disponibles:

- Suma de polinomios  
- Multiplicación de polinomios  
- Derivación de un polinomio  
- Integración de un polinomio  
- Evaluación de un polinomio

---

### 🔹 Módulo de Vectores

Opciones disponibles:

- Suma de vectores  
- Resta de vectores  
- Magnitud de un vector  
- Producto punto  
- Producto cruzado

---

### 🔹 Módulo de Derivación e Integración

Permite calcular **derivadas** e **integrales** de funciones simbólicas ingresadas por el usuario.

---

### 🔹 Módulo de Gráficas 2D y 3D

Permite graficar funciones en 2D y 3D de una o más variables. El usuario puede ingresar funciones personalizadas para su visualización gráfica.

---

### 🔹 Módulo "Acerca de"

Muestra la información académica del autor y detalles del proyecto:

- **Nombre del autor**: Gómez Molina José Andrés  
- **Carrera**: Ingeniería en Software  
- **Semestre**: 6to  
- **Año académico**: 2025  
- **Materia**: Modelos Matemáticos y Simulación  
- **Profesor**: Ing. Morales Torres Isidro Fabricio

---

## ✅ Recomendaciones

- Usar Python 3.8 o superior.
- Verificar que los módulos estén correctamente instalados antes de generar el `.exe`.
- Ejecutar el `.exe` desde la carpeta `dist/`, donde se crean los recursos y el ejecutable.

---

## 📁 Estructura recomendada del proyecto

```
calculadora-cientifica/
│
├── app.py
├── styles.css
├── images/
│   ├── logo.png
│   └── fondo.jpg
├── README.md
└── dist/
    └── app.exe
```

---

¡Gracias por usar esta calculadora científica! Cualquier duda o sugerencia puede comunicarse con el autor.
