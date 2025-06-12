from flask import Flask, jsonify
from flask_cors import CORS
from data_parser import parse_all_conferences # 引入新的解析器

app = Flask(__name__)
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
    all_conferences = parse_all_conferences()
    print(f"Parser finished, found {len(all_conferences)} conferences.")
    return jsonify(all_conferences)

if __name__ == '__main__':
    # 监听所有网络接口，而不仅仅是本地回环地址
    app.run(host='0.0.0.0', debug=True) 