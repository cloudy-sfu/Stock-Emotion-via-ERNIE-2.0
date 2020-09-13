import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sn
import pickle as pkl
from sklearn.model_selection import train_test_split

df = pd.read_excel("data/db_3_features.xlsx")
df.dropna(inplace=True)
print(df.shape)
print(df.columns)

fig = plt.figure(figsize=(12, 9))
sn.heatmap(df.corr(), cmap="Blues")
fig.savefig("results/db_3_overview.png")

Xur_c = df[['attw_read', 'attw_cmt',
            'attw_following', 'attw_follower', 'attw_av', 'attw_tv',
            'p1cr', 'p2cr', 'p3cr', 'p4cr', 'p5cr', 'p1ta',
            'p2ta', 'p3ta', 'p4ta', 'p5ta']]
Xr_c = df[['p1cr', 'p2cr', 'p3cr', 'p4cr', 'p5cr', 'p1ta',
           'p2ta', 'p3ta', 'p4ta', 'p5ta']]
Y_c = df['close_rate']

Xur_c_train, Xur_c_valid, Xr_c_train, Xr_c_valid, Y_c_train, Y_c_valid = \
    train_test_split(Xur_c, Xr_c, Y_c, train_size=0.8)
with open("results/db_reg_close", "wb") as f:
    pkl.dump([Xur_c_train, Xur_c_valid, Xr_c_train, Xr_c_valid, Y_c_train, Y_c_valid], f)
