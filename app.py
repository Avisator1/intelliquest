from flask import Flask, render_template, request, jsonify, redirect, url_for
from PIL import Image

from io import BytesIO
import openai
import requests


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


@app.route('/send_text', methods=['POST'])
def send_text():
    selected_text = request.form.get('text')
    print(selected_text)

    url = 'http://75.28.163.79:6069/api/generate'

    def ollama(model, prompt):
        request_data = {"model": model,
                        "prompt": prompt,
                        "stream": False
                        }
        response = requests.post(url, json=request_data)
        response.raise_for_status()    
        output = response.json()["response"]
        response.close()

        return output

    solved_text = ollama("llama2", f"Give me a very short 2 sentences explanation of this question that I am showing you after this period. {selected_text}")
    print(solved_text)

    # Return JSON response
    return jsonify({'solved_text': solved_text})


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=80)
