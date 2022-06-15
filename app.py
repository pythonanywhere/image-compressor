#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

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


#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
current_wd = os.getcwd()
image_directory = os.path.join(current_wd, "images")
uncompressed_directory = os.path.join(image_directory, "uncompressed")
compressed_directory = os.path.join(image_directory, "compressed")
#db = SQLAlchemy(app)

# Automatically tear down SQLAlchemy.
'''
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
'''

# Login required decorator.
'''
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap
'''
#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/joseph_fourier')
def joseph_fourier():
    return render_template('JF.html')

@app.route('/serie_fourier')
def serie_fourier():
    return render_template('SF.html')

@app.route('/compresion')
def compresion():
    return render_template('compresion.html')

@app.route('/fft')
def fft():
    return render_template('fft.html')

@app.route('/fft2', methods=["POST"])
def fft2():
    perc = 0.1
    file = request.files["the_file"]
    file_name = os.path.join(uncompressed_directory, file.filename)
    file.save(file_name)
    A = imread(file_name)

    B = np.mean(A, -1)
    Bt = np.fft.fft2(B)
    Btsort = np.sort(np.abs(Bt.reshape(-1)))
    thresh = Btsort[int(np.floor((1-perc)*len(Btsort)))]
    ind = np.abs(Bt)>thresh
    Atlow = Bt * ind
    Alow = np.fft.ifft2(Atlow).real
    img = Image.fromarray(Alow)
    img = img.convert("L")
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
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
