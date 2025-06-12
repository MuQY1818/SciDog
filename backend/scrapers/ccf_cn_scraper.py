import requests
import re
import ast
import json

# 数据源：一个纯净的 HTML 表格页面，但数据实际在<script>标签中
URL = "https://ccfddl.cn/"

def scrape_ccf_data_from_script():
    """
    通过解析 <script> 标签中的 JavaScript 变量来爬取会议信息
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(URL, headers=headers, timeout=20)
        response.raise_for_status()
        response.encoding = 'utf-8'
        
        html_content = response.text
        
        # 使用正则表达式找到所有 rows.push({...}) 的调用
        # re.DOTALL 使得 '.' 可以匹配包括换行符在内的任意字符
        pattern = re.compile(r"rows\.push\((.*?)\)", re.DOTALL)
        matches = pattern.findall(html_content)
        
        conferences = []
        for match in matches:
            try:
                # match 是一个形如 {'key':'value', ...} 的字符串
                # ast.literal_eval 可以安全地将这个字符串转为 Python 字典
                conf_dict = ast.literal_eval(match)
                conferences.append(conf_dict)
            except (ValueError, SyntaxError) as e:
                print(f"解析单条会议数据时出错: {match}, 错误: {e}")
                continue
                
        return conferences

    except requests.exceptions.RequestException as e:
        print(f"获取网页时发生错误: {e}")
        return []
    except Exception as e:
        print(f"处理时发生未知错误: {e}")
        return []

if __name__ == '__main__':
    print("开始从 script 标签爬取 ccfddl.cn ...")
    all_conferences = scrape_ccf_data_from_script()
    if all_conferences:
        print(f"成功爬取到 {len(all_conferences)} 个会议信息。")
        # 打印前5个会议作为示例
        print(json.dumps(all_conferences[:5], indent=2, ensure_ascii=False))
    else:
        print("未能爬取到任何会议信息。") 