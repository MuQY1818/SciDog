from flask import Flask, jsonify
from flask_cors import CORS
from data_parser import parse_all_conferences

app = Flask(__name__)
CORS(app)

# Cache the loaded data to avoid parsing on every request
_conference_data = None

def load_conferences():
    """Loads and caches conference data from the parser."""
    global _conference_data
    if _conference_data is None:
        print("Parsing conference data from source YAML files...")
        _conference_data = parse_all_conferences()
        print("Conference data loaded and cached successfully.")
    return _conference_data

@app.route('/api/conferences', methods=['GET'])
def get_conferences():
    """Endpoint to get the conference data."""
    data = load_conferences()
    return jsonify(data)

if __name__ == '__main__':
    # Load data on startup
    load_conferences()
    # Run the Flask app
    app.run(debug=True, port=5000) 