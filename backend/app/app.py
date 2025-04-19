from flask import Flask, jsonify
from flask_cors import CORS
import json
import os

def load_superheroes():
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(current_dir, 'superheroes.json')
        with open(json_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: superheroes.json file not found")
        return []
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in superheroes.json")
        return []
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return []

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
    app.run(debug=True, port=3000)
