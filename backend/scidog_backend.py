import json
import os
import sys
import yaml
import glob
import re
from datetime import datetime

# ==============================================================================
# Functions previously in data_parser.py are now merged into this file
# to avoid ModuleNotFound errors in the CI/CD environment.
# ==============================================================================

def get_type_mapping():
    """
    从 README.zh-CN.md 文件中解析出 sub-category 的中文映射。
    """
    readme_path = os.path.join(os.path.dirname(__file__), 'data_source', 'README.zh-CN.md')
    mapping = {}
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        table_section_start = content.find('类别匹配表:')
        if table_section_start == -1:
            print("Warning: '类别匹配表:' not found in README.zh-CN.md")
            return {}
            
        table_content = content[table_section_start:]
        
        pattern = re.compile(r"\|\s*`(\w+)`\s*\|\s*(.*?)\s*\|")
        matches = pattern.findall(table_content)
        
        for match in matches:
            sub_code = match[0].strip()
            name = match[1].strip()
            if sub_code and name and sub_code.lower() != 'sub':
                mapping[sub_code] = name
                
    except Exception as e:
        print(f"Error parsing type mapping from README: {e}")
        return {}
        
    return mapping


def parse_all_conferences():
    """
    遍历 data_source/conference 目录，解析所有 yaml 文件,
    并转换成前端需要的格式。
    """
    type_mapping = get_type_mapping()
    base_path = os.path.join(os.path.dirname(__file__), 'data_source', 'conference')
    all_files = glob.glob(f'{base_path}/**/*.yml', recursive=True)
    
    conferences_list = []
    
    for file_path in all_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                yaml_content = yaml.safe_load(f)
                if not yaml_content:
                    continue

                if isinstance(yaml_content, dict):
                    yaml_content = [yaml_content]

                for conf_series in yaml_content:
                    if not isinstance(conf_series, dict):
                        continue

                    series_title = conf_series.get('title', 'N/A')
                    series_desc = conf_series.get('description', '')
                    series_sub = conf_series.get('sub', '').upper()
                    series_rank = conf_series.get('rank', {})
                    
                    if 'confs' in conf_series and isinstance(conf_series['confs'], list):
                        for conf_instance in conf_series['confs']:
                            if not isinstance(conf_instance, dict): continue

                            deadline = 'TBD'
                            if 'timeline' in conf_instance and isinstance(conf_instance['timeline'], list):
                                valid_deadlines = [
                                    item['deadline'] for item in conf_instance['timeline'] 
                                    if isinstance(item,dict) and item.get('deadline') and 'TBD' not in str(item.get('deadline')).upper()
                                ]
                                if valid_deadlines:
                                    deadline = max(valid_deadlines)
                                elif conf_instance['timeline']:
                                    first_event = conf_instance['timeline'][0]
                                    deadline = first_event.get('deadline', 'TBD') if isinstance(first_event, dict) else 'TBD'

                            ccf_rank = series_rank.get('ccf', 'N') if isinstance(series_rank, dict) else 'N'
                            
                            conference_item = {
                                'id': conf_instance.get('id', f'{series_title}-{conf_instance.get("year", "N/A")}'),
                                'title': series_title,
                                'subname': type_mapping.get(series_sub, series_sub),
                                'description': series_desc,
                                'ccfRank': ccf_rank,
                                'type': series_sub,
                                'year': conf_instance.get('year', 'N/A'),
                                'date': conf_instance.get('date', 'N/A'),
                                'place': conf_instance.get('place', 'N/A'),
                                'link': conf_instance.get('link', '#'),
                                'deadline': str(deadline),
                                'timezone': conf_instance.get('timezone', 'UTC')
                            }
                            if conference_item.get('title') and conference_item['title'] != 'N/A':
                                conferences_list.append(conference_item)
                    
                    else:
                        deadline = conf_series.get('deadline', 'TBD')
                        if 'timeline' in conf_series and isinstance(conf_series['timeline'], list):
                            valid_deadlines = [
                                item['deadline'] for item in conf_series['timeline'] 
                                if isinstance(item,dict) and item.get('deadline') and 'TBD' not in str(item.get('deadline')).upper()
                            ]
                            if valid_deadlines:
                                deadline = max(valid_deadlines)
                            elif conf_series['timeline']:
                                first_event = conf_series['timeline'][0]
                                deadline = first_event.get('deadline', 'TBD') if isinstance(first_event, dict) else 'TBD'

                        ccf_rank = series_rank.get('ccf', 'N') if isinstance(series_rank, dict) else 'N'

                        conference_item = {
                            'id': conf_series.get('id', f'{series_title}-{conf_series.get("year", "N/A")}'),
                            'title': series_title,
                            'subname': type_mapping.get(series_sub, series_sub),
                            'description': series_desc,
                            'ccfRank': ccf_rank,
                            'type': series_sub,
                            'year': conf_series.get('year', 'N/A'),
                            'date': conf_series.get('date', 'N/A'),
                            'place': conf_series.get('place', 'N/A'),
                            'link': conf_series.get('link', '#'),
                            'deadline': str(deadline),
                            'timezone': conf_series.get('timezone', 'UTC')
                        }
                        if conference_item.get('title') and conference_item['title'] != 'N/A':
                            conferences_list.append(conference_item)

            except yaml.YAMLError as e:
                print(f"Error parsing YAML file {file_path}: {e}")
            except Exception as e:
                print(f"An unexpected error occurred with file {file_path}: {e}")

    now = datetime.now()

    def sort_key(conf):
        deadline_str = conf.get('deadline', 'TBD')
        if deadline_str.upper() == 'TBD' or not isinstance(deadline_str, str):
            return (2, now)

        try:
            deadline_date = datetime.strptime(deadline_str, '%Y-%m-%d %H:%M:%S')
            if deadline_date < now:
                return (1, deadline_date)
            else:
                return (0, deadline_date)
        except ValueError:
            try:
                deadline_date = datetime.strptime(deadline_str.split()[0], '%Y-%m-%d')
                if deadline_date < datetime.combine(now.date(), datetime.min.time()):
                     return (1, deadline_date)
                else:
                     return (0, deadline_date)
            except ValueError:
                 return (2, now)

    conferences_list.sort(key=sort_key)

    return {
        "conferences": conferences_list,
        "type_mapping": type_mapping
    } 

# ==============================================================================
# Original script logic starts here
# ==============================================================================

def generate_static_json():
    """
    调用 data_parser 来生成最新的数据，并将其保存为
    一个静态的 JSON 文件，供前端直接使用。
    """
    print("Generating static JSON data for frontend using data_parser...")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, '..', 'frontend', 'public', 'conferences.json')
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    data_to_save = parse_all_conferences()
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data_to_save, f, ensure_ascii=False, indent=2)
        
    print(f"Successfully generated conferences.json at: {output_path}")


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'generate':
        generate_static_json()
    else:
        from flask import Flask, jsonify
        from flask_cors import CORS

        app = Flask(__name__)
        CORS(app)

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