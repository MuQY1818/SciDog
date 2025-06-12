from flask import Flask, jsonify
from flask_cors import CORS
from data_parser import parse_all_conferences
import os

app = Flask(__name__)
# 为整个应用开启 CORS 支持
CORS(app)

@app.route('/api/conferences')
def get_conferences():
    """
    Main API endpoint to get all conference data.
    """
    data = parse_all_conferences()
    return jsonify(data)

# This is the entry point for Vercel
# The file is named `app.py`, and the Flask app object is named `app`.
# Vercel's Python runtime will automatically find it.

if __name__ == '__main__':
    # 监听所有网络接口，而不仅仅是本地回环地址
    app.run(host='0.0.0.0', debug=True) 