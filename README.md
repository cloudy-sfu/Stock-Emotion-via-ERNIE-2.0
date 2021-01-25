# Stock Emotion via ERNIE 2.0
![](https://img.shields.io/badge/build-developing-brightgreen)
![](https://img.shields.io/badge/tests-2020.8.14-orange)
![](https://img.shields.io/badge/dependencies-eastmoney.com-blue)
![](https://img.shields.io/badge/dependencies-paddlepaddle-blue)

This repository is a research, with comments from `eastmoney.com`, to evaluate the strength of people's positive or negative sentiment towards a certain stock. The outline of this research is as follows.

## Acknowledges
[SKEP model](https://www.paddlepaddle.org.cn/hubdetail?name=ernie_skep_sentiment_analysis&en_category=SentimentAnalysis)

[random forest regressor](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html#sklearn.ensemble.RandomForestRegressor.score)

[Bayes search](https://scikit-optimize.github.io/stable/modules/generated/skopt.BayesSearchCV.html)

## 1. Data pre-processing
### 1.1. Collect the list of comments
Run `post_panel.py`, setting `n_pages`, creating an empty folder `posts_raw` to store the results, and use the list of `data/000905closeweight.xlsx`. This script allows me to get the list of comments.

Then, run `concat_raw_panels.py` to concatenate these lists into a single table. In the table, I filter the comments with some rules, which are recorded at sheet `description`. The results are saved in `data/db_1_panel.xlsx`.

### 1.2. Collect the information of authors of the comments
Run `post_author.py` to get the ids of authors from `data/db_1_panel.xlsx`, and collect 4 attributes of each author (follower, following, number of visits to his/her homepage of all time, that of today), where the data not available are filled with `None`. The results are saved to a temporary file.

### 1.3. Collect the main body of the comments
Run `post_content.py` to get the hyperlink of comments. Due to the `eastmoney.com`'s limitation to robots, I cannot get all comments. Instead, ads and promotions are collected.

Firstly, I store all of them to a temporary file. Secondly, I use regex to replace the elements that are not real comments with `None`. The patterns of ads and promotions are like:
```
[下载查看原文]    'NoneType'    HTTPSError    今日(6月30日)
```
and blanks.

It should to be noticed that, since I need to concatenate the info of authors, main body and other info in the comments list, I just replace unexpected data to `None` instead of deleting them. As a result, the length of each table is the same.

### 1.4. Generate the clean data table
I concatenate the 3 files, and drop the absent values (including `None` just assigned). In addition, I manually filter the table with some rules, which are recorded at `description` sheet either. A column `stock` is added, according to the principle of hyperlink of the man body of each comment. Specifically speaking, the hyperlink follows
```
https://guba.eastmoney.com/news,[stock code],[a random integer].html
```
So, I can know which stock does each comment refer.

The filtered data table is `data/db_2_full.xlsx`.

|                         | Attributes                                                 | Data Type |
| ----------------------- | ---------------------------------------------------------- | --------- |
| read                    | The times it is read.                                      | int       |
| comment                 | Number of replies to the comment                           | int       |
| update                  | Last update time                                           | datetime  |
| following               | Number of people the author follows                        | int       |
| follower                | Number of the author's followers                           | int       |
| author_all_visit        | Total number of visits                                     | int       |
| author_today_visit_0814 | Number of visits on a single day (counted on Aug 14, 2020) | int       |
| context                 | The entire content of the comment                          | string    |
| stock                   | The code of the stock reviewed by the comment              | string    |

## 2. Nature language processing
### 2.1. Introduction of the pre-trained model
In this section, I use SKEP model and porn detection model to draw out the emotion contained in comments. To recurrent the results, you need to install it. It is adopted to predict whether the attitude of each comment is positive or negative.

Note: Since the training of NLP models is expensive and time-consuming, meanwhile I have limited financial support, I choose to use pre-trained model released by Baidu PaddlePaddle. All the results is based on the trust to the accuracy and scientific of SKEP model.

### 2.2. Fix the packages
For computers with GPU, the original package requires GPU device name to be added to environment variables. It bothers, so I simplify it. To make use of it, replace `~/.paddlehub/modules/ernie_skep_sentiment_analysis/module.py` with `package_fixed/skep/module.py`.

### 2.3. Usage
Run `senta_1.py` to use this model to process natural language. I use the model to scale the degree of optimistic attitude in each comment. The result is saved as a column added to the data table in section 1.4. It ranges from 0 to 1, which means the probability that a sample is positive. High value indicates the sample is more optimistic.

## 3. Predict the stock price
### 3.1. Sampling
The table `RESSET_QTTN_2016__1.xlsx` contains the price and trading amount of all stocks listed from July 1 to July 28, 2020. The date range of comments is from July 11 to July 27, 2020. The price data has a little wider time range, so some features like "the rate of return of previous 5 days" can be included.

Run `sampling.py` to extract the features. The result would be saved in `data/db_3_features.xlsx`. The table of features looks like:

|                | Attribute                                                    | Data Type |
| -------------- | ------------------------------------------------------------ | --------- |
| stock          | Stock code.                                                  | string    |
| date           | The predicted day.                                           | datetime  |
| open_rate      | Rate of return, compering open price and previous close price. | float     |
| close_rate     | Rate of return, compering close price and previous close price. | float     |
| attw_read      | Attitude weighted by the times it is read. It means the degree of positive attitude of comments posted 1 day before the predicted day. | float     |
| attw_cmt       | Attitude weighted by the times it is replied.                | float     |
| attw_following | Attitude weighted by number of people the author follows.    | float     |
| attw_follower  | Attitude weighted by the author's followers.                 | float     |
| attw_av        | Attitude weighted by total number of visits to the author.   | float     |
| attw_tv        | Attitude weighted by the number of visits to the author on a singe day (counted on Aug 14, 2020). | float     |
| p1or           | Open rate of 5 days ago (before the predicted day).          | float     |
| p2or           | Open rate of 4 days ago.                                     | float     |
| p3or           | Open rate of 3 days ago.                                     | float     |
| p4or           | Open rate of 2 days ago.                                     | float     |
| p5or           | Open rate of 1 day ago.                                      | float     |
| p1cr           | Close rate of 5 days ago.                                    | float     |
| p2cr           | Close rate of 4 days ago.                                    | float     |
| p3cr           | Close rate of 3 days ago.                                    | float     |
| p4cr           | Close rate of 2 days ago.                                    | float     |
| p5cr           | Close rate of 1 day ago.                                     | float     |
| p1ta           | Log trading amount of 5 days ago.                            | float     |
| p2ta           | Log trading amount of 4 days ago.                            | float     |
| p3ta           | Log trading amount of 3 days ago.                            | float     |
| p4ta           | Log trading amount of 2 days ago.                            | float     |
| p5ta           | Log trading amount of 1 day ago.                             | float     |

### 3.2. Random forest model

Run `close_prepare.py` to make the datasets, and run `close_rf_1.py` to use the random forest model.

To perform the regressions mentioned above via random forest model are adopted and their results are compared. Bayes search with 5-fold cross validation is also adopted, and the optimal model is finally accepted. MSE is the metric to evaluate the performance of each model.

The data is divided into 80% training set and 20% validation set, and the 5-fold cross validation  is constructed based on the training set.

### 3.3. Significance test

I build the unrestricted model and restricted model, to find out whether the attitudes weighted by those attributes are significant in predicting the stock price. The tasks are separated into the regression of open rate and the regression of close rate.

For open rate:
```
UR: open_rate ~ att* + pior + pita
R: open_rate ~ pior + pita
```
For close rate:
```
UR: open_rate ~ att* + picr + pita
R: open_rate ~ picr + pita
```

Note: `pi` means the list from `p1` to `p5`, `att*` means the attitudes weighted by other attributes.

The F-statistic is used to test the significance. Because the heteroscedasticity has limited effect on random forest models, so the F-statistic
$$F=\frac{(R_{ur}^2 - R_r^2)(n-k-1)}{(1-R_{ur}^2)q}$$
is adopted to test the significance. In the equation q is the number of variables different between UR and R models, and k is the number of variables in UR model. Although $R^2$ is defined in linear models, as the documentation of random forest regressor introduced, the `score` method of it returns $R^2$. And this metric is adopted in this research.

Todo: Estimate the effect, which the heteroscedasticity contributes to random forest models.

Run `close_estimate.py` to perform the F-stats test.
