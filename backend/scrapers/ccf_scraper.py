import requests
from bs4 import BeautifulSoup

# 中国计算机学会推荐国际学术会议和期刊目录 (2022)
URL = "https://www.ccf.org.cn/kyhd/gyml/20221222/845455.shtml"

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
        
        # 网页内容是 gbk 编码, 需要正确解码
        response.encoding = 'gbk'
        
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"获取网页时发生错误: {e}")
        return None

def parse_page(html_content):
    """
    解析 HTML 内容并提取信息 (目前只打印标题)
    """
    if not html_content:
        return

    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 打印网页标题以作验证
    print(f"网页标题: {soup.title.string}")
    
    # TODO: 在这里添加提取会议列表的逻辑

if __name__ == '__main__':
    html = fetch_ccf_page()
    parse_page(html) 