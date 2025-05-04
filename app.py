from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

DATA_FILE = 'movies.json'

# Load movie data from file
def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

# Save movie data to file
def save_data(movies):
    with open(DATA_FILE, 'w') as f:
        json.dump(movies, f, indent=2)

@app.route('/movies', methods=['GET'])
def get_movies():
    user = request.args.get('user')
    if not user:
        return jsonify({'error': 'User required'}), 400

    movies = load_data()
    user_movies = [m for m in movies if m['user'] == user]
    return jsonify(user_movies)

@app.route('/movies', methods=['POST'])
def add_movie():
    movie = request.get_json()
    movies = load_data()
    movie['id'] = max([m['id'] for m in movies], default=0) + 1
    movies.append(movie)
    save_data(movies)
    return jsonify({'message': 'Movie added'}), 201

@app.route('/movies/<int:movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    user = request.args.get('user')
    if not user:
        return jsonify({'error': 'User required'}), 400

    movies = load_data()
    updated_movies = [m for m in movies if not (m['id'] == movie_id and m['user'] == user)]
    save_data(updated_movies)
    return jsonify({'message': 'Movie deleted'})

if __name__ == '__main__':
    app.run(debug=True)