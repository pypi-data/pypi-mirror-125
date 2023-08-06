import numpy as np
import pandas as pd
import chart_studio
import matplotlib.pyplot as plt
from plotly import graph_objs as go
import sklearn
import seaborn as sns
import itertools

def plot_results(x_values, y_init_concat, y_pred_concat, zoomable=False):
    # Use of classic motplotlib
    if not zoomable:
        plt.subplots(figsize=(10, 4))
        plt.plot(x_values, y_init_concat, label='truth')  # , marker='o')
        plt.plot(x_values, y_pred_concat, label='prediction')  # , marker='o')
        plt.legend()
        plt.show()

    # Use of Plotly
    else:
        temp_real = go.Scatter(
            x=pd.Series(x_values),
            y=pd.Series(y_init_concat))

        temp_predict = go.Scatter(
            x=pd.Series(x_values),
            y=pd.Series(y_pred_concat))

        data = [temp_real, temp_predict]
        chart_studio.plotly.iplot(data, world_readable=True)

    return None


def regression(regr, X_train, X_test, y_train, y_test):
    print('Train :', X_train.shape, 'Test : ', X_test.shape, 'Total :', X_train.shape[0] + X_test.shape[0])
    regr.fit(X_train, y_train)

    y_pred_train = regr.predict(X_train)
    train_score = display_scores(y_train, y_pred_train, 'TRAIN')

    y_pred_test = regr.predict(X_test)
    test_score = display_scores(y_test, y_pred_test, 'TEST')  # , mape=True, tmp=test_set)

    return y_pred_train, y_pred_test, train_score, test_score, regr


def MASE_score(testing_series, prediction_series):
    """
    Computes the MEAN-ABSOLUTE SCALED ERROR forcast error for univariate time series prediction. 
    See "Another look at measures of forecast accuracy", Rob J Hyndman
    parameters:
        training_series: the series used to train the model, 1d numpy array
        testing_series: the test series to predict, 1d numpy array or float
        prediction_series: the prediction of testing_series, 1d numpy array (same size as testing_series) or float
        absolute: "squares" to use sum of squares and root the result, "absolute" to use absolute values.
    
    """
    diff = testing_series - prediction_series
    n = diff.shape[0]
    print('%' * 10, n)
    d = np.abs(diff).sum() / (n - 1)

    errors = np.abs(testing_series - prediction_series)
    return errors.mean() / d


def MAPE(y_true, y_pred):
    return np.max(np.abs((y_true - y_pred) / y_true)) * 100


def display_scores(y, y_pred, name='Dataset', mape=False, tmp=False, cut=3):
    nb_stars = 5
    print('\n', '*' * nb_stars, name, '*' * nb_stars)

    # RMSE
    rmse = np.sqrt(sklearn.metrics.mean_squared_error(y, y_pred))  # metrics.roc_auc_score(y_test,pred[:,1])
    print('RMSE', np.round(rmse, cut))

    # Mean Error
    mean_error = np.sum(np.abs((y_pred - y))) / len(y_pred)
    print('Mean', np.round(mean_error, cut))

    # MASE
    mase = MAPE(y - y.shift(-8 * 6 * 6), y, y_pred)
    print('MASE', np.round(mase, cut))

    # MAPE
    if mape and tmp is not None:
        mape = MAPE(y + tmp.temperature_smooth, y_pred + tmp.temperature_smooth)
        print('MAPE', np.round(mape, cut))

    return rmse, mean_error, mase


# def select_regr_model(mdl=0):
#     if mdl == 0:
#         return SVR()
#     if mdl == 1:
#         return SVR(gamma='scale', C=1.0, epsilon=0.2)
#     if mdl == 2:
#         return RandomForestRegressor(max_depth=6, random_state=1, n_estimators=60, min_samples_split=4)
#     if mdl == 3:
#         return Ridge(alpha=1.0)
#     if mdl == 4:
#         return ElasticNet()
#     return Lasso


def split_train_test(df):
    # Select temporal range
    start_date = pd.to_datetime('20170115')
    end_date = pd.to_datetime('20180501')

    # Separating dataset into two
    train_set = df[(df.datetime > start_date) &
                   (df.datetime < end_date)].copy()

    test_set = df[df.datetime > end_date].copy()
    return train_set, test_set


# i = 1
# _ = plt.figure(figsize=(20, 10))
# for type_ in df_pred.type.unique():
#     _ = plt.subplot(3, 3, i)
#     df_pred.loc[df_pred['type'] == type_, 'y_reel'].hist(label='reel')
#     df_pred.loc[df_pred['type'] == type_, 'y_pred'].hist(label='pred')
#     _ = plt.title(type_)
#     i += 1
# _ = plt.legend()
# _ = plt.show()


# # Plotting it
# _ = sns.countplot(df_train['isFraud'])
# _ = plt.title('Répartion des fraudes')
# _ = plt.show()


# # Visualisation of missing values
# _ = plt.figure(figsize=(20, 8))
# _ = sns.barplot(y=df_train.isnull().sum().sort_values(ascending=False),
#                 x=df_train.isnull().sum().sort_values(ascending=False).index)
# _ = plt.title("Counts of missing value in df_train", size=20)
# _ = plt.xticks(fontsize=7)
# _ = plt.xticks(rotation=90)
# _ = plt.show()


def plot_hist(train, colname):
    """f.plot_hist(df_train, 'TransactionAmt')
    """
    _train_0 = train[train['isFraud'] == 0].reset_index(drop=False)
    _train_1 = train[train['isFraud'] == 1].reset_index(drop=False)
    _ = plt.figure(figsize=(20, 7))  # facecolor='w')
    ax = sns.kdeplot(_train_0[colname], color='b', alpha=0.4, shade=True)
    ax_2 = ax.twinx()
    _ = sns.kdeplot(_train_1[colname], color='r', alpha=0.4, shade=True, ax=ax_2)
    _ = ax.set_title(colname)
    _ = plt.show()


def plot_distribution_amount(df):
    # f.plot_distribution_amount(df_train)

    df1 = df[df['isFraud'] == 0]
    not_fraud = df1['TransactionAmt'].apply(np.log)  # we will apply log transformation to get better visualization

    df2 = df[df['isFraud'] == 1]
    fraud = df2['TransactionAmt'].apply(np.log)  # we will apply log transformation to get better visualization

    _ = plt.figure(figsize=(20, 7))
    _ = sns.distplot(a=not_fraud, label='Not Fraud')
    _ = sns.distplot(a=fraud, label='Fraud')
    _ = plt.legend()
    _ = plt.show()


def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j],
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')


def visualize_numeric_columns(df, num_cols, x=3, y=3):
    _ = plt.figure(figsize=(20, 15))
    j = 1
    for i in num_cols:
        _ = plt.subplot(x, y, j)
        _ = sns.distplot(a=df[i])
        j = j + 1
    _ = plt.show()


# def plot_auc(reg, X_test, y_test, model_name='Logistic Regression'):
#     # Calculating output porbas and ROC Metrics
#     y_pred_prob = reg.predict_proba(X_test)[:, 1]
#     fpr, tpr, thresholds = roc_curve(y_test, y_pred_prob)
#
#     # PLotting results
#     plt.plot([0, 1], [0, 1], 'k--')
#     plt.plot(fpr, tpr, label=model_name)
#     plt.xlabel('False Positive Rate')
#     plt.ylabel('True Positive Rate')  # Is also the Recall
#     plt.title('{} ROC Curve'.format(model_name))
#     plt.show()
#
#     # Caluclation AUC Score
#     auc_score = roc_auc_score(y_test, y_pred_prob)
#     print('The AUC Score is {}'.format(auc_score))
#
#     # Calculating CV-AUC Score
#     # cv_auc_scores = cross_val_score(reg,X,y,cv=5,scoring='roc_auc')
#     # print("AUC scores computed using 5-fold cross-validation: \n{}".format(cv_auc_scores))
