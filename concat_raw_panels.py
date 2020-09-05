import os
import pandas as pd

folder = "./posts_raw/"
post_separate = os.listdir(folder)

df = [pd.read_excel(folder + f) for f in post_separate]
df = pd.concat(df)
df.to_excel("./data/post_panel_all.xlsx", index=False)
