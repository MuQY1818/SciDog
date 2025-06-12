import requests
from bs4 import BeautifulSoup

# 数据源来自: https://ccf.atom.im/
# 这是一个整理好的 CCF 目录网页，比官方的 PDF 更容易解析
URL = "https://ccf.atom.im/"

def fetch_ccf_page():
    """
    获取 CCF 推荐目录的网页内容
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(URL, headers=headers, timeout=10)
        response.raise_for_status()  # 如果请求失败 (状态码不是 2xx), 会抛出异常
        
        # 该网页编码是 utf-8
        response.encoding = 'utf-8'
        
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"获取网页时发生错误: {e}")
        return None

def parse_page(html_content):
    """
    解析 HTML 内容并提取会议信息
    """
    if not html_content:
        return []

    soup = BeautifulSoup(html_content, 'html.parser')
    
    conferences = []
    
    # 通过分析网页源码，我们发现所有会议信息都在一个 <tbody> 元素里
    # 我们可以直接找到所有的 <tr> (table row) 标签
    table_rows = soup.select("tbody > tr")

    # 我们需要一个变量来追踪当前正在处理的专业领域
    current_field = ""

    for row in table_rows:
        cols = row.find_all('td')
        
        # CCF 目录按领域划分，有些行是标题行，需要特殊处理
        # 标题行的 <strong> 标签里是领域名称
        header = row.find('strong')
        if header:
            current_field = header.text.strip()
            continue

        # 确保行中有足够的列来提取数据
        if len(cols) == 5:
            conference = {
                'id': cols[0].text.strip(),
                'abbr': cols[1].text.strip(),
                'full_name': cols[2].text.strip(),
                'category': cols[3].text.strip(),
                'field': current_field # 使用我们追踪的领域名称
            }
            conferences.append(conference)

    return conferences

if __name__ == '__main__':
    html = fetch_ccf_page()
    conference_list = parse_page(html)
    
    # 打印前5个会议，验证一下结果
    for conf in conference_list[:5]:
        print(conf) 