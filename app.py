from flask import Flask, render_template, request, jsonify, redirect, url_for
import base64
import re
from PIL import Image
import fitz
import pytesseract
import easyocr
from io import BytesIO
import openai

app = Flask(__name__)

openai.api_key = "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"


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

@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    try:
        data = request.get_json()
        pdf_data = data.get('pdfData')

        # Decode base64 and create a PDF document
        pdf_bytes = pdf_data.split(',')[1].encode('utf-8')
        pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")

        # Extract text from the PDF
        text = ""
        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            text += page.get_text()

        pdf_document.close()

        # Redirect to problems.html with the extracted text
        return redirect(url_for('problems', text=text))

    except Exception as pdf_error:
        print(f'Error processing PDF: {str(pdf_error)}')
    return jsonify({'success': False, 'message': f'Error processing PDF: {str(pdf_error)}'})


@app.route('/problems')
def problems():
    text = request.args.get('text', '')  # Get the extracted text from the URL parameter
    return render_template('problems.html', text=text)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=80)
