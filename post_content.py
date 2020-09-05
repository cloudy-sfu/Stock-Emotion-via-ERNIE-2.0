from requests import Session
from bs4 import BeautifulSoup
import pandas as pd
import pickle
import re

ms_edge = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,en-GB;q=0.6',
    'Connection': 'keep-alive',
    'Host': 'guba.eastmoney.com',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/84.0.4147.105 Safari/537.36 Edg/84.0.522.58 '
}

post_menu = pd.read_excel("data/db_1_panel.xlsx")
content_menu = post_menu['正文链接']


def get_content(url):
    print(url)
    try:
        session = Session()
        html = session.get(url, headers=ms_edge, timeout=5)
        content = BeautifulSoup(html.text, features="html.parser").find('div', class_='stockcodec .xeditor')
        return content.text
    except Exception as e:
        return e.__str__()


content_all = [get_content(x) for x in content_menu]
content_all = [re.sub(r'\s', '', x) for x in content_all]
with open("data/post_content_sub_1", "wb") as f:
    pickle.dump(content_all, f)
