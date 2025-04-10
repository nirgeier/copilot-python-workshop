from flask import Flask, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

# Load superheroes data using path relative to this file
current_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(current_dir, 'superheroes.json')
with open(json_path, 'r') as f:
    superheroes = json.load(f)

@app.route('/')
def hello():
    return "Save the World!"

@app.route('/superheroes/all')
def get_all_superheroes():
    return jsonify(superheroes)

@app.route('/superheroes/<int:hero_id>')
def get_superhero(hero_id):
    hero = next((hero for hero in superheroes if hero['id'] == hero_id), None)
    if hero is None:
        return jsonify({'error': 'Superhero not found'}), 404
    return jsonify(hero)

@app.route('/superheroes/<int:hero_id>/powerstats')
def get_superhero_stats(hero_id):
    hero = next((hero for hero in superheroes if hero['id'] == hero_id), None)
    if hero is None:
        return jsonify({'error': 'Superhero not found'}), 404
    return jsonify(hero['powerstats'])

if __name__ == '__main__':
    app.run(debug=True)