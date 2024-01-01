from flask import Flask, render_template, request, jsonify
import base64
import re
from PIL import Image
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

@app.route("/upload_image", methods=["POST"])
def upload_image():
    data = request.get_json()

    if "imageDataUrl" in data:
        # Decode base64-encoded image data
        image_data = data["imageDataUrl"].split(",")[1].encode("utf-8")
        img = Image.open(BytesIO(base64.b64decode(image_data)))

        # Perform OCR using Tesseract
        text = perform_ocr(img)

        # Categorize the problem based on keywords
        category = categorize_problem(text)

        # Formulate a prompt for OpenAI
        prompt = f"Solve the following {category} problem: {text}"

        # Make a request to OpenAI API
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=50  # Adjust as needed
        )

        # Extract the generated text from OpenAI's response
        generated_text = response["choices"][0]["text"].strip()

        return jsonify({"problem_text": text, "category": category, "solution": generated_text})

    return jsonify({"error": "No image data provided"}), 400

def perform_ocr(image):
    # Perform OCR using Tesseract
    text = pytesseract.image_to_string(image)

    return text

def categorize_problem(text):
    # Use regular expressions to identify simple math expressions
    math_expression_pattern = re.compile(r'\b\d+(\s*[\+\-\*/\^]\s*\d+)+\b')

    # Keywords related to geometry
    geometry_keywords = ["triangle", "circle", "rectangle", "area", "perimeter", "angle"]

    text_lower = text.lower()

    # Check if it's a mathematical expression
    if math_expression_pattern.search(text):
        return "math"
    
    # Check if it contains geometry keywords
    elif any(keyword in text_lower for keyword in geometry_keywords):
        return "geometry"
    
    else:
        return "uncategorized"

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=80)
