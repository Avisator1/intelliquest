from flask import Flask, render_template, request, jsonify
import base64
from PIL import Image
import pytesseract
from io import BytesIO

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

@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'imageDataUrl' in request.json:
        # Decode the base64 image data and save it
        image_data = request.json['imageDataUrl'].split(',')[1]
        image_binary = base64.b64decode(image_data)

        # Save the image for debugging (optional)
        with open('uploaded_image.jpg', 'wb') as f:
            f.write(image_binary)

        # Perform OCR on the image
        image = Image.open(BytesIO(image_binary))
        extracted_text = pytesseract.image_to_string(image, lang='eng')

        return jsonify({'status': 'success', 'text': extracted_text})

    return jsonify({'status': 'error', 'message': 'No image data uploaded'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=80)
