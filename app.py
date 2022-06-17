# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

from unittest import result
from flask import Flask, render_template, request, send_file

# from flask.ext.sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from forms import *
import os
import numpy as np
from matplotlib.image import imread
import matplotlib.pyplot as plt
from PIL import Image


# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object("config")
current_wd = os.getcwd()
static_directory = os.path.join(current_wd, "static")
image_directory = os.path.join(static_directory, "images")
uncompressed_directory = os.path.join(image_directory, "uncompressed")
compressed_directory = os.path.join(image_directory, "compressed")
# db = SQLAlchemy(app)

# Automatically tear down SQLAlchemy.
"""
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
"""

# Login required decorator.
"""
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap
"""
# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/joseph_fourier")
def joseph_fourier():
    return render_template("JF.html")


@app.route("/serie_fourier")
def serie_fourier():
    return render_template("SF.html")


@app.route("/compresion")
def compresion():
    return render_template("compresion.html")


@app.route("/fft")
def fft():
    return render_template("fft.html")


@app.route("/fft2", methods=["POST"])
def fft2():
    # perc es la variable que determina el porcentaje de coeficientes que se mantendrán

    perc = request.form.get("number")
    
    # Si el usuario nos dio un porcentaje de coeficientes usaremos eso sino probaremos con 4 diferentes porcentaje
    # 10% 5% 1% y 0.5%
    porcentajes = [int(perc)/100] if perc else [0.1, 0.05, 0.01, 0.005]

    # obtenemos el archivo a partir del formulario, viene etiquetado con ´the_file´ en compresion.html
    file = request.files["the_file"]

    # definimos la ruta del lugar donde guardaremos este archivo, en este caso lo guardaremos a nuestro directorio de imagenes no comprimidas
    file_name = os.path.join(uncompressed_directory, file.filename)

    # guardamos nuestro archivo a dicha ruta
    file.save(file_name)

    # Calculamos el tamaño en Bytes de la imagen original
    original_file_size = os.stat(file_name).st_size  # número de Bytes

    # Utilizando la función imread volvemos a abrir nuestro archivo
    A = imread(file_name)

    # Hacemos una reducción de dimensiones sencilla. Una imagen RGB tiene 5 dimensiones (altura, ancho, R, G, B). Hacemos el promedio de RGB para tener sólo un número
    # El resultado de esto es una imágen en escala de grises pero ahora sólo con 2 dimensiones (altura y ancho)
    B = np.mean(A, -1)

    # Procedemos a realizar la FFT2 (en este caso necesitamos la versión bidimensional porque es una señal bidimensional).
    # Esto es el equivalente de hacer FFT por todas las columns y luego todos los renglones o viceversa.
    Bt = np.fft.fft2(B)  # Bt al ser la transformada es una matriz de números complejos

    # Convertimos nuestra matriz a un arreglo unidimensional y calculamos las magnitudes de nuestros números complejos
    magnitudes = np.abs(Bt.reshape(-1))

    # Ordenamos nuestro arreglo del más pequeño al más grande (ascendente)
    Btsort = np.sort(magnitudes)

    comprimidas = []
    # Por cada porcentaje de coeficientes haremos las operaciones y guardaremos los resultados en 'comprimidas'
    for keep in porcentajes:
        # Calculamos el porcentaje de los valores que despreciaremos. Si sólo queremos el 10%, eliminaremos el 90%
        # np.floor redondea al número más bajo, con el fin de tener un número entero.
        cantidad_a_eliminar = int(np.floor((1 - keep) * len(Btsort)))

        # El número anterior lo usaremos como índice y así obtener el coeficiente que representa el límite inferior de los coeficientes que mantendremos
        limite = Btsort[cantidad_a_eliminar]

        # A partir de este límite crearemos una máscara determinando aquellos coeficiente que no son despreciables.
        # ind es una matriz del mismo tamaño que Bt (transformada de B)
        # pero con valores booleanos (que pueden ser interpretados como respondiendo la pregunta '¿este coeficiente es suficientemente grande/relevante para mantener en la memoria?')
        ind = np.abs(Bt) > limite

        # Usaremos la mascara ind para eliminar aquellos valores muy pequeños para ser importantes. En este caso eliminar es volver cero.
        # Esto se hace mediante el producto punto de matrices.
        # Al final tenemos una matriz del mismo tamaño que Bt pero sólo con coeficientes grandes.
        Atlow = Bt * ind

        # Hacemos la transformada inversa para regresar el dominio original
        Alow = np.fft.ifft2(Atlow).real

        # Convertimos nuestra matriz de números a una imagen de escala de grises (porque ya no tenemos los tres canales RGB)
        img = Image.fromarray(Alow)
        img = img.convert("L")

        # Guardamos la imagen en el directorio de imagenes comprimidas
        compressed_file_name = os.path.join(compressed_directory, f"{keep}_{file.filename}")
        img.save(compressed_file_name)

        # Aquí calculamos el tamaño en Bytes de la imagen comprimida razones demostrativas
        result_file_size = os.stat(compressed_file_name).st_size  # en Bytes

        # Guardamos la ruta de nuestra imagen comprimida junto con su tamaño en nuestra lista
        comprimidas.append(
            {
                "ruta": f"/static/images/compressed/{keep}_{file.filename}",
                "bytes": f"{result_file_size:,}"
            }
        )

    return render_template(
        "comparacion.html",
        file=f"/static/images/uncompressed/{file.filename}",
        compressed_files=comprimidas,
        original_file_size=f"{original_file_size:,}",
    )

# @app.route('/login')
# def login():
#     form = LoginForm(request.form)
#     return render_template('forms/login.html', form=form)


# @app.route('/register')
# def register():
#     form = RegisterForm(request.form)
#     return render_template('forms/register.html', form=form)


# @app.route('/forgot')
# def forgot():
#     form = ForgotForm(request.form)
#     return render_template('forms/forgot.html', form=form)

# # Error handlers.


# @app.errorhandler(500)
# def internal_error(error):
#     #db_session.rollback()
#     return render_template('errors/500.html'), 500


# @app.errorhandler(404)
# def not_found_error(error):
# return render_template('errors/404.html'), 404

if not app.debug:
    file_handler = FileHandler("error.log")
    file_handler.setFormatter(
        Formatter("%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]")
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info("errors")

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == "__main__":
    app.run()

# Or specify port manually:
"""
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
"""
