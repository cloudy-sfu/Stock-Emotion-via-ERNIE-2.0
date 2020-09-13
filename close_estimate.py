import pickle as pkl

with open("results/db_reg_close", "rb") as f:
    Xur_c_train, Xur_c_valid, Xr_c_train, Xr_c_valid, Y_c_train, Y_c_valid = pkl.load(f)
with open("results/UR_close_rf_1", "rb") as f:
    ur_model = pkl.load(f)
with open("results/R_close_rf_1", "rb") as f:
    r_model = pkl.load(f)

Rur2 = ur_model.score(Xur_c_valid, Y_c_valid)
Rr2 = r_model.score(Xr_c_valid, Y_c_valid)
k = Xur_c_valid.shape[1]
n = Xur_c_valid.shape[0]
q = k - Xr_c_valid.shape[1]
f_stats = (Rur2 - Rr2) * (n - k - 1) / (1 - Rur2) / q
print(f'F statistic: {f_stats}')

# %%
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sn


def color_barplot_en(name_, score_, title, size):
    plt.rcParams['axes.unicode_minus'] = False
    fig = plt.figure(figsize=size)
    ax = sn.barplot(x=score_, y=np.arange(score_.shape[0]), orient='h', palette="Blues_r")
    ax.set_title(title)
    ax.set_yticklabels(name_)
    return fig


ur_feat_score = ur_model.best_estimator_.feature_importances_
r_feat_score = r_model.best_estimator_.feature_importances_
ur_fig = color_barplot_en(Xur_c_valid.columns, ur_feat_score, "Feature Importance of Unrestricted Model", (6, 4))
ur_fig.savefig("results/close_rf_1_ur_featimp.png")
r_fig = color_barplot_en(Xr_c_valid.columns, r_feat_score, "Feature Importance of Restricted Model", (6, 4))
r_fig.savefig("results/close_rf_1_r_featimp.png")

# %%
print(ur_feat_score)
print(r_feat_score)
print(ur_model.best_estimator_.max_depth, r_model.best_estimator_.max_depth)
print(Rur2, Rr2)
