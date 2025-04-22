


Código necesario para instalar todos los módulos requeridos:

pip install pyqt5 matplotlib numpy sympy

Instalar para poer hacer el ejecutable .exe:

Abra su terminal de cu compilador, en este caso VScode crtl+ñ:

pip install pyinstaller

Una vez instalado use el siguente comando para hacer el ejecutable:

pyinstaller --noconfirm --windowed --onefile --add-data "images;images" --add-data "styles.css;." app.py
