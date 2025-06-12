from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from data_parser import parse_all_conferences
import os

app = Flask(__name__, static_folder='../frontend/dist')
# 为整个应用开启 CORS 支持
CORS(app)

@app.route("/")
def hello_world():
    return "<p>Hello, SciDog! This is the backend server.</p>"

@app.route("/api/conferences")
def get_conferences():
    """
    提供会议数据的 API 端点。
    它会实时运行爬虫并返回最新的数据。
    """
    print("Received request for /api/conferences. Parsing from local YAML files...")
    data = parse_all_conferences()
    print(f"Parser finished, found {len(data)} conferences.")
    return jsonify(data)

# Serve a specific file from the static folder
@app.route('/assets/<path:filename>')
def serve_assets(filename):
    return send_from_directory(os.path.join(app.static_folder, 'assets'), filename)

# Serve the main index.html for any other route
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    # 监听所有网络接口，而不仅仅是本地回环地址
    app.run(host='0.0.0.0', debug=True) 