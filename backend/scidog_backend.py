import json
import os
import sys
# 从 data_parser.py 导入核心数据解析函数
from data_parser import parse_all_conferences

def generate_static_json():
    """
    调用 data_parser 来生成最新的数据，并将其保存为
    一个静态的 JSON 文件，供前端直接使用。
    """
    print("Generating static JSON data for frontend using data_parser...")
    
    # 定义输出路径
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, '..', 'frontend', 'public', 'conferences.json')
    
    # 确保目标目录存在
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # 调用解析器获取数据
    data_to_save = parse_all_conferences()
    
    # 保存数据到静态 JSON 文件
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data_to_save, f, ensure_ascii=False, indent=2)
        
    print(f"Successfully generated conferences.json at: {output_path}")


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'generate':
        generate_static_json()
    else:
        # --- Flask App related imports and setup ---
        # These are only imported when running the web server, not during static generation.
        from flask import Flask, jsonify
        from flask_cors import CORS

        app = Flask(__name__)
        CORS(app)

        # 缓存加载的数据，避免每次请求都重新解析
        _conference_data = None

        def load_conferences():
            global _conference_data
            if _conference_data is None:
                print("Parsing conference data from source files...")
                _conference_data = parse_all_conferences()
                print("Conference data loaded and cached.")
            return _conference_data

        @app.route('/api/conferences', methods=['GET'])
        def get_conferences():
            data = load_conferences()
            return jsonify(data)

        print("Starting Flask server...")
        app.run(debug=True) 