from flask import Flask, render_template, request, jsonify, redirect, url_for
import base64
import re
from PIL import Image
import fitz
import pytesseract
import pymongo
import easyocr
from io import BytesIO
import openai

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', home=True)

@app.route('/login')
def login():
    return render_template('login.html', login=True)

@app.route('/register')
def register():
    return render_template('register.html', register=True)

@app.route('/getstarted')
def started():
    return render_template('started.html', started=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=80)
