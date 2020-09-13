import pickle as pkl
from skopt import BayesSearchCV
from sklearn.ensemble import RandomForestRegressor
from skopt.space import Real, Categorical, Integer

with open("results/db_reg_close", "rb") as f:
    Xur_c_train, Xur_c_valid, Xr_c_train, Xr_c_valid, Y_c_train, Y_c_valid = pkl.load(f)

ur_model = BayesSearchCV(
    RandomForestRegressor(oob_score=True),
    {
        'max_depth': Integer(10, 30),
    },
    n_iter=32, verbose=1,
    cv=5
)
ur_model.fit(Xur_c_train, Y_c_train)
with open("results/UR_close_rf_1", "wb") as f:
    pkl.dump(ur_model, f)

r_model = BayesSearchCV(
    RandomForestRegressor(oob_score=True),
    {
        'max_depth': Integer(10, 30),
    },
    n_iter=32, verbose=1,
    cv=5
)
r_model.fit(Xr_c_train, Y_c_train)
with open("results/R_close_rf_1", "wb") as f:
    pkl.dump(r_model, f)
