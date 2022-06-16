# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

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
image_directory = os.path.join(current_wd, "images")
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
    perc = 0.1

    # obtenemos el archivo a partir del formulario, viene etiquetado con ´the_file´ en compresion.html
    file = request.files["the_file"]

    # definimos la ruta del lugar donde guardaremos este archivo, en este caso lo guardaremos a nuestro directorio de imagenes no comprimidas
    file_name = os.path.join(uncompressed_directory, file.filename)

    # guardamos nuestro archivo a dicha ruta
    file.save(file_name)

    # Utilizando la función imread volvemos a abrir nuestro archivo
    A = imread(file_name)

    # Hacemos una reducción de dimensiones sencilla. Una imagen RGB tiene 5 dimensiones (altura, ancho, R, G, B). Hacemos el promedio de RGB para tener sólo un número
    # El resultado de esto es una imágen en escala de grises pero ahora sólo con 2 dimensiones (altura y ancho)
    B = np.mean(A, -1)

    # Procedemos a realizar la FFT2 (en este caso necesitamos la versión bidimensional porque es una señal bidimensional). 
    # Esto es el equivalente de hacer FFT por todas las columns y luego todos los renglones o viceversa.
    Bt = np.fft.fft2(B) # Bt al ser la transformada es una matriz de números complejos

    # Convertimos nuestra matriz a un arreglo unidimensional y calculamos las magnitudes de nuestros números complejos
    magnitudes = np.abs(Bt.reshape(-1))

    # Ordenamos nuestro arreglo del más pequeño al más grande (ascendente)
    Btsort = np.sort(magnitudes)

    # Calculamos el porcentaje de los valores que despreciaremos. Si sólo queremos el 10%, eliminaremos el 90%
    # np.floor redondea al número más bajo, con el fin de tener un número entero.
    cantidad_a_eliminar = int(np.floor((1 - perc) * len(Btsort)))

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
    file_name = os.path.join(compressed_directory, file.filename)
    img.save(file_name)
    return send_file(file_name, mimetype=file.content_type)


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
