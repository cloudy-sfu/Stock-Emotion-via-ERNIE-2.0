# %%
import numpy as np
import pandas as pd

price = pd.read_excel("data/RESSET_QTTN_2016__1.xlsx", dtype={"date": "datetime64"})
comment = pd.read_excel("data/db_2_simplified.xlsx", dtype={"date": "datetime64"})


def w(x_array, weight):
    if np.sum(weight) == 0:
        return 0
    rst_raw = np.sum(x_array * weight) / np.sum(weight)
    return float(rst_raw)


b_date = pd.bdate_range(start="2020-07-01", end="2020-07-30")
t_date = np.unique(comment['date']) + pd.to_timedelta(1, unit='days')
t_price = price[price['date'].isin(t_date)]

new_comment = []
for _, x in t_price.iterrows():
    b_date_id = np.sum(b_date < x.date)
    previous_5_date = b_date[b_date_id - 5:b_date_id]  # business day
    previous_1_date = x.date - pd.to_timedelta(1, unit='days')
    c = comment[(comment['stock'] == x.stock_code) & (comment['date'] == previous_1_date)]
    previous_price = price[(price['stock_code'] == x.stock_code) & (price['date'].isin(previous_5_date))]
    # 5 day open rate (from earlier to later)
    pvor = (previous_price.open - previous_price.previous_close) / previous_price.previous_close
    # 5 day close rate (from earlier to later)
    pvcr = (previous_price.close - previous_price.previous_close) / previous_price.previous_close
    # 5 day trading amount (from earlier to later)
    pvta = np.log(previous_price.trading)
    x = [
            x.stock_code,
            x.date,  # date of predicted tomorrow
            (x.open - x.previous_close) / x.previous_close,  # open rate
            (x.close - x.previous_close) / x.previous_close,  # close rate
            w(c.attitude, c.read),  # attitude weighted by read
            w(c.attitude, c.comment),  # attitude weighted by comment
            w(c.attitude, c.following),  # attitude weighted by following
            w(c.attitude, c.follower),  # attitude weighted by follower
            w(c.attitude, c.author_all_visit),  # attitude weighted by all visit
            w(c.attitude, c.author_today_visit_0814)  # attitude weighted by today visit
        ] + pvor.to_list() + pvcr.to_list() + pvta.to_list()  # log trading amount
    new_comment.append(x)

new_comment = pd.DataFrame(
    data=new_comment,
    columns=['stock', 'date', 'open_rate', 'close_rate',
             'attw_read', 'attw_cmt', 'attw_following', 'attw_follower',
             'attw_av', 'attw_tv',
             'p1or', 'p2or', 'p3or', 'p4or', 'p5or',
             'p1cr', 'p2cr', 'p3cr', 'p4cr', 'p5cr',
             'p1ta', 'p2ta', 'p3ta', 'p4ta', 'p5ta'],
)
new_comment.to_excel("data/db_3_features.xlsx", index=False)
