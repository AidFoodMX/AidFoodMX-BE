from flask import Flask, jsonify
from flask_cors import CORS
from app.routes import register_routes

app = Flask(__name__)

# Apply CORS to the entire app
CORS(app)  # This allows CORS for all routes

register_routes(app)

if __name__ == '__main__':
    app.run(debug=True)
