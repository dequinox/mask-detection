import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template, jsonify
from werkzeug.utils import secure_filename
import pathlib
from flask_cors import CORS
from config import *
from utils import *
import base64
import cv2

from maskDetect import MaskDetector

mask = MaskDetector('last_copy.pt', 'output')

app = Flask(__name__, static_url_path='/static')
CORS(app)
app.config['UPLOAD_FOLDER'] = 'output'

def convert_and_save(b64_string):
    b64_string = b64_string[b64_string.find(",") + 1:]
    with open("images/sample_image.jpg", "wb") as fh:
        fh.write(base64.decodebytes(b64_string.encode()))

@app.route('/uploads/<filename>', methods=['GET'])
def uploaded_file(filename):
    # process image from MODEL
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        convert_and_save(request.json['image64'])
        img = mask.detect_mask('images/sample_image.jpg')
        retval, buffer = cv2.imencode('.jpg', img)
        jpg_as_text = base64.b64encode(buffer)
        return jpg_as_text
        # return send_from_directory(app.config['UPLOAD_FOLDER'], 'sample_image.jpg')

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)