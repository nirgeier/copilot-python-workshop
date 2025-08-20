from flask import Flask, jsonify
from flask_cors import CORS
import json
import os

def load_superheroes():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, 'superheroes.json')
    with open(json_path, 'r') as f:
        return json.load(f)

app = Flask(__name__)
CORS(app)

superheroes = load_superheroes()

@app.route('/')
def hello():
    return "Save the World!"

@app.route('/superheroes/all')
def get_all_superheroes():
    return jsonify(superheroes)

if __name__ == '__main__':
    app.run(debug=True, port=3000, host='0.0.0.0')
