from flask import Flask, render_template, request, jsonify, redirect, url_for
from io import BytesIO
import requests


app = Flask(__name__)
app.config['SECRET_KEY'] = 'JRWIOARJOWRJWOIRJWOIRJAWIORJIWRJAWIORJWIORJIWORJAWIORJWIORJWIORJAWOIRJAOWRJORJOWRJOWRJOWRJWRDAWFGGH'
@app.route('/')
def index():
    return render_template('index.html', home=True)


@app.route('/getstarted')
def started():
    return render_template('started.html', started=True)


@app.route('/send_text', methods=['POST'])
def send_text():
    selected_text = request.form.get('text')
    print(selected_text)

    url = ''

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

    solved_text = ollama("llama2", f"Hi Ollama, i am about to ask you a question and i need you to follow this critera: dont repeat the question which i ask, and just provide the answer and the explanation and nothing else. The question will be present after this period. {selected_text}")
    print(solved_text)

    return jsonify({'solved_text': solved_text})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
