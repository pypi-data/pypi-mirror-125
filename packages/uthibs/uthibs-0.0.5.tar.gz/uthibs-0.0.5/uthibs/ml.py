import time
import numpy as np
import pandas as pd

from sklearn.model_selection import KFold
from sklearn.metrics import mean_absolute_error


def compute_log_score(X_test_type, y_test, y_pred):
    df = pd.concat([X_test_type.reset_index(drop=True), y_test.reset_index(drop=True), pd.Series(y_pred)], axis=1)
    df.columns = ['type', 'test', 'pred']
    score = 0
    for type_ in df.type.unique():
        tmp = df[df['type'] == type_]
        tmp['diff'] = tmp['test'] - tmp['pred']
        tmp['abs'] = np.abs(tmp['diff'])
        total = tmp['abs'].sum()
        moyenne = total / tmp.shape[0]
        moyenne_log = np.log(moyenne)
        score += moyenne_log
    score = score / df.type.nunique()
    return np.round(score, 4)


def cross_val_sk_learn(X, y, cv, model, score_metric=mean_absolute_error, round_=4):
    score_train = []
    score_test = []
    folds = KFold(n_splits=5, shuffle=True, random_state=20)

    for fold_n, (train_index, test_index) in enumerate(folds.split(X)):
        print('Fold', fold_n, 'started at', time.ctime())
        X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]

        model.fit(X_train, y_train)

        y_pred_test = model.predict(X_test)
        y_pred_train = model.predict(X_train)

        train_score = np.round(score_metric(y_pred_train, y_train), round_)
        test_score = np.round(score_metric(y_pred_test, y_test), round_)
        # print('Score for train set: ', train_score)
        # print('Score for test set: ', test_score)
        score_train.append(train_score)
        score_test.append(test_score)
        # print('-----------------------------------------')
    print('Average score for train set: ', np.mean(score_train))
    print('Average score for test set: ', np.mean(score_test))
    print('Copyright Noctis')
    return score_train, score_test
