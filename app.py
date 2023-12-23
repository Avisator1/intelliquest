from flask import Flask, render_template, request
import base64
from PIL import Image
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/image', methods=['POST'])
def image():
    data = request.get_json() 
    result = data['imageData']
    image_data = base64.b64decode(result)
    image = Image.open(BytesIO(image_data))
    image = image.convert('RGB')

    image.save("output_image.jpg")

    return "Image received and checking for Math"

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
