from flask import Flask, jsonify
from flask_cors import CORS

# 从我们的爬虫脚本中导入函数
from scrapers.ccf_cn_scraper import scrape_ccf_data_from_script

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
    print("Received request for /api/conferences. Running scraper...")
    conferences = scrape_ccf_data_from_script()
    print(f"Scraper finished, found {len(conferences)} conferences.")
    return jsonify(conferences)

if __name__ == '__main__':
    # 监听所有网络接口，而不仅仅是本地回环地址
    app.run(host='0.0.0.0', debug=True) 