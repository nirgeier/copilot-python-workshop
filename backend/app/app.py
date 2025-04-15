from flask import Flask, jsonify, request
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

# This is a superheroes API server that supports multiple endpoints
# The data is stored in a JSON file in the project folder called superheroes.json
# 1. /superheroes/all - returns a list of all superheroes, as a JSON array
# 2. /superheroes/:id - returns a specific superhero by id, as a JSON object
# 3. /superheroes/:id/powerstats - returns the powers statistics for superhero by id, as a JSON object
# 4. /superheroes/:id/assign-team - assigns a superhero to a team
# 5. /superheroes/team/:team_name - returns all superheroes belonging to a specific team

superheroes = load_superheroes()

@app.route('/')
def hello():
    return "Save the World!"

@app.route('/superheroes/all')
def get_all_superheroes():
    """
    Get a list of all superheroes.

    Returns:
        json: A JSON array containing all superhero objects from the superheroes list.
        Each superhero object contains hero information such as name, powers, etc.
    """
    return jsonify(superheroes)

@app.route('/superheroes/<int:id>')
def get_superhero_by_id(id):
    """
    Get a superhero by ID.

    Args:
        id (int): The ID of the superhero.

    Returns:
        json: A JSON object containing the superhero information.
        If the superhero is not found, returns a 404 error.
    """
    for hero in superheroes:
        if hero['id'] == id:
            return jsonify(hero)
    return jsonify({"error": "Superhero not found"}), 404

@app.route('/superheroes/<int:id>/powerstats')
def get_superhero_powerstats_by_id(id):
    """
    Get the power statistics of a superhero by ID.

    Args:
        id (int): The ID of the superhero.

    Returns:
        json: A JSON object containing the power statistics of the superhero.
        If the superhero is not found, returns a 404 error.
    """
    for hero in superheroes:
        if hero['id'] == id:
            return jsonify(hero['powerstats'])
    return jsonify({"error": "Superhero not found"}), 404

@app.route('/superheroes/<int:id>/assign-team', methods=['PUT'])
def assign_team(id):
    """
    Assign a superhero to a team.

    Args:
        id (int): The ID of the superhero.

    Returns:
        json: A JSON object containing the updated superhero information.
        If the superhero is not found, returns a 404 error.
    """
    team_data = request.get_json()
    if not team_data or 'team' not in team_data:
        return jsonify({"error": "Team name is required"}), 400

    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, 'superheroes.json')

    for hero in superheroes:
        if hero['id'] == id:
            hero['team'] = team_data['team']
            with open(json_path, 'w') as f:
                json.dump(superheroes, f, indent=2)
            return jsonify(hero)
    return jsonify({"error": "Superhero not found"}), 404

@app.route('/superheroes/team/<team_name>')
def get_superheroes_by_team(team_name):
    """
    Get all superheroes belonging to a specific team.

    Args:
        team_name (str): The name of the team.

    Returns:
        json: A JSON array containing all superhero objects from the specified team.
    """
    team_heroes = [hero for hero in superheroes if hero.get('team', '').lower() == team_name.lower()]
    if not team_heroes:
        return jsonify({"error": "No superheroes found for this team"}), 404
    return jsonify(team_heroes)

if __name__ == '__main__':
    app.run(debug=True, port=3000)
