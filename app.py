import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename
import pathlib
from flask_cors import CORS
from config import *
from utils import *

app = Flask(__name__, static_url_path='/static')
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/uploads/<filename>', methods=['GET'])
def uploaded_file(filename):
    # process image from MODEL
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        return request.json
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)