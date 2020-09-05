# %%
from datetime import datetime
from urllib import parse

import pandas as pd
from bs4 import BeautifulSoup
from requests import Session

# %%

df = pd.read_excel("data/db_1_panel.xlsx")


# %%%

def get_author(url_id):
    url = f"https://i.eastmoney.com/{int(url_id)}"
    print(url)
    now = datetime.now()
    st_sp = parse.quote(now.strftime("%Y-%m-%d %H:%M:%S"))
    st_psi = now.strftime("%Y%m%d%H%M%S%MS")

    ms_edge = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/'
                  'signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,en-GB;q=0.6',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'qgqp_b_id=aae44f1324a9a242a206b37652874f28; st_si=47894910145512; st_sn=1; '
                  f'st_psi={st_psi}-1190142302762-8137242326; st_asi=delete; st_pvi=16486913011041; '
                  f'st_sp={st_sp}; st_inirUrl=',
        'Host': 'i.eastmoney.com',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/84.0.4147.105 Safari/537.36 Edg/84.0.522.58',
    }

    session = Session()
    html = session.get(url, headers=ms_edge)
    try:
        html = BeautifulSoup(html.text, features='html.parser').find('div', class_='others_content')
        following = html.find('a', id="tafollownav").span.text
        follower = html.find('a', id="tafansa").span.text
        all_visit, today_visit = [x.text for x in html.find('div', class_="others_info").find_all('span')[:2]]
    except:
        return
    return following, follower, all_visit, today_visit


author = [get_author(x) for x in df['作者编号']]
author = pd.DataFrame(author, columns=['following', 'follower', 'all_visit', 'today_visit'])
author.to_csv("data/post_author_sub_1", index=False)
