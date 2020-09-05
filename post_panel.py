from requests import Session
from datetime import datetime
from urllib import parse
from bs4 import BeautifulSoup
import re
import pandas as pd
import logging

now = datetime.now()
st_sp = parse.quote(now.strftime("%Y-%m-%d %H:%M:%S"))
st_psi = now.strftime("%Y%m%d%H%M%S%MS")

ms_edge = {
    'Host': 'guba.eastmoney.com',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/84.0.4147.89 Safari/537.36 Edg/84.0.522.40',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9',
}

logging.basicConfig(filename="./posts_raw/eastmoney_log", filemode="a")


def get_post_panel(code, page):
    index_url = f"http://guba.eastmoney.com/list,{code}_{page}.html"
    quote_index_url = parse.quote(index_url)
    list_header = {**ms_edge,
                   'Cookie': 'st_si=34728572543791;st_asi=delete;qgqp_b_id=40eef261b49920a68b88f70a5b799044;'
                             f'st_pvi=86043649387334; st_sp={st_sp}; st_inirUrl={quote_index_url}; st_sn=3; '
                             f'st_psi={st_psi}-117001301474-6547216362',
                   }
    session = Session()
    req_index = session.get(index_url, headers=list_header)
    index = BeautifulSoup(req_index.text, features="lxml").find('div', id='articlelistnew')
    if not index:
        logging.warning(f"评论版面获取失败, 股票{code}, 页码{page}.")
        return pd.DataFrame(columns=["阅读量", "评论数", "标签", "标题", "正文链接", "作者编号", "最后更新"])
    posters = [
        index_inline_transformer(x)
        for x in index.find_all('div', class_=re.compile(r'articleh'))
        if not x.find('em', class_='settop')
    ]
    return pd.DataFrame(
        data=posters, columns=["阅读量", "评论数", "标签", "标题", "正文链接", "作者编号", "最后更新"]
    )


def index_inline_transformer(a_poster):
    reading = a_poster.find('span', class_="l1 a1").text
    reading = int(eval(re.sub('万', '*10000', reading)))
    replies = int(a_poster.find('span', class_="l2 a2").text)
    labels = a_poster.em.text if a_poster.find('em') else ''
    title = a_poster.find('span', class_="l3 a3").a.text
    content_link = a_poster.find('span', class_="l3 a3").a.get("href")
    author_id = a_poster.find('span', class_='l4 a4').a.get("data-popper")
    update = a_poster.find('span', class_='l5 a5').text
    return [reading, replies, labels, title, content_link, author_id, update]


if __name__ == '__main__':
    code_list = list(pd.read_excel("./data/000905closeweight.xlsx", converters={'成分券代码Constituent Code': str})
                     ['成分券代码Constituent Code'])
    n_pages = 10
    for code in code_list:
        posters_stock = [get_post_panel(code, x) for x in range(1, n_pages + 1)]
        posters_stock = pd.concat(posters_stock)
        posters_stock.to_excel(f"./posts_raw/{code}_1_{n_pages}.xlsx", index=False)
        print(f"FINISH: {code}")
