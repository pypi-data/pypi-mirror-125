import copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.linear_model import Lasso
from sklearn.model_selection import TimeSeriesSplit
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error


# from pandas.plotting import register_matplotlib_converters
# register_matplotlib_converters()

# # Next steps :
# - Documentation of functions
# - Create a ReadMe
# - Add a function for saving object 

class TimeSerieCrossVal:

    def __init__(self, split_number=10, regr=None, verbose=0, title='Default_title'):
        self.title = title
        self.verbose_ = verbose
        self.verbose('Init {}'.format(title), 1)
        self.score_dict = {}
        self.split_number = split_number
        self.splitter = self.initSplit(split_number)
        self.data = {'X': None, 'y': None, 'predict_by_model': None}
        self.x_split_range = None

        if regr is None:
            self.is_regr = False
        else:
            self.is_regr = True
            self.regr = copy.deepcopy(regr)

    def verbose(self, text, lvl=10):
        if self.verbose_ == -1:
            print(text)
        elif lvl <= self.verbose_:
            print(text)

    def initSplit(self, split_number):
        self.verbose('Le dataset sera séparé en {} parties.'.format(split_number), 1)
        tscv = TimeSeriesSplit(n_splits=split_number)
        return tscv

    def addRegr(self, regr):
        self.verbose('Ajout d\'un modèle de régression personnalisé.', 1)
        self.verbose(regr, 2)
        self.regr = regr
        self.is_regr = True

    def delRegr(self):
        self.verbose('Supression du modèle de régression.', 1)
        self.regr = None
        self.is_regr = False

    def addDefaultRegr(self, id_=2):
        self.verbose('Ajout d\'un modèle de régression par défaut : ({})'.format(id_), 1)
        if (id_ == 1) or (id_ == 'rf_deep'):
            self.regr = RandomForestRegressor(max_depth=4, random_state=1, n_estimators=90, min_samples_split=4)
            self.is_regr = True
        if (id_ == 2) or (id_ == 'lasso'):
            self.regr = Lasso(alpha=1)
            self.is_regr = True
        if (id_ == 3) or (id_ == 'rf'):
            self.regr = RandomForestRegressor(max_depth=2, random_state=1, n_estimators=20, min_samples_split=2)
            self.is_regr = True

    def MASE(self, diff, testing_series, prediction_series):
        n = diff.shape[0]
        d = np.abs(diff).sum() / (n - 1)
        errors = np.abs(testing_series - prediction_series)
        return errors.mean() / d

    def MAPE(self, y_train, y_pred):
        return np.max(np.abs((y_train - y_pred) / y_train)) * 100

    def displayScores(self, y_train, y_pred, name='Dataset', mase_=True, mape=False, tmp=False, cut=3):

        # Computing
        # print('DISPLAY SCORES RMSE', y_train.values, y_pred)
        rmse = np.sqrt(mean_squared_error(y_train.values, y_pred))  # metrics.roc_auc_score(y_test,pred[:,1])
        # print('rmse', rmse)
        mean_error = np.sum(np.abs((y_pred - y_train))) / len(y_pred)
        if mase_:
            mase = self.MASE(y_train - y_train.shift(-8 * 6 * 6), y_train, y_pred)
        if mape and tmp is not None:
            mape = self.MAPE(y_train + tmp.temperature_smooth, y_pred + tmp.temperature_smooth)

        # Displaying
        nb_stars = 5
        stars_line = '*' * nb_stars
        self.verbose('\n {} {} {}'.format(stars_line, name, stars_line), 2)
        self.verbose('RMSE : {}'.format(np.round(rmse, cut)), 2)
        self.verbose('Mean : {}'.format(np.round(mean_error, cut)), 2)
        if mase_:
            self.verbose('MASE : {}'.format(np.round(mase, cut)), 2)
        if mape and tmp is not None:
            self.verbose('MAPE : {}'.format(np.round(mape, cut)), 2)

        if mase_:
            return rmse, mean_error, mase
        return rmse, mean_error

    def regression(self, X_train, X_test, y_train, y_test):
        self.verbose('Starting regression', 2)
        regressor = copy.deepcopy(self.regr)
        regressor.fit(X_train, y_train)
        y_pred_train = regressor.predict(X_train)
        y_pred_test = regressor.predict(X_test)
        self.verbose(regressor, 3)
        self.verbose('Ending regression', 2)
        return (y_pred_train, y_pred_test, regressor)

    def fit(self, X, y, compute_mase_=True):
        if not self.is_regr:
            self.addDefaultRegr(2)
        self.data['X'] = X.copy()
        self.data['y'] = y.copy()
        self.verbose('Dimension X : {}'.format(X.shape), 1)
        self.verbose('Dimension y : {}'.format(y.shape), 1)
        self.score_dict = {}
        self.x_split_range = None

        id_model = 0
        for _, test_index in self.splitter.split(X):
            self.verbose('Iteration : {}/{}'.format(id_model + 1, self.split_number), 1)

            # Separating train/test datasets
            X_train_cv, X_test_cv = X.iloc[:test_index[0]], X.iloc[test_index[0]:test_index[-1]]
            y_train_cv, y_test_cv = y.iloc[:test_index[0]], y.iloc[test_index[0]:test_index[-1]]

            # Printing information about split£
            self.verbose('Dimensions de X_train {}'.format(X_train_cv.shape), 2)
            self.verbose('Dimensions de X_test  {}'.format(X_test_cv.shape), 2)
            self.verbose('Dimensions de y_train {}'.format(y_train_cv.shape), 2)
            self.verbose('Dimensions de y_test  {}'.format(y_test_cv.shape), 2)

            # Calculating 
            regr_result = self.regression(X_train_cv, X_test_cv, y_train_cv, y_test_cv)
            y_pred_train = regr_result[0]
            y_pred_test = regr_result[1]
            regressor = copy.deepcopy(regr_result[2])

            # Storing results
            ans = {'y_pred_train': y_pred_train,
                   'y_pred_test': y_pred_test,
                   'train_score': self.displayScores(y_train_cv, y_pred_train, 'TRAIN', mase_=compute_mase_),
                   'test_score': self.displayScores(y_test_cv, y_pred_test, 'TEST', mase_=compute_mase_),
                   # , mape=True, tmp=test_set)],
                   'regr': regressor}
            self.score_dict[id_model] = ans
            id_model += 1

        self.x_split_range = [value['y_pred_train'].shape[0] for key, value in self.score_dict.items()]

    def plotScores(self, test=True, train=False, rmse_=True, mean_=False):
        # %matplotlib inline
        _ = plt.subplots(figsize=(20, 5))

        if test:
            if rmse_:
                _ = plt.plot(self.x_split_range, [value['test_score'][0] for key, value in self.score_dict.items()],
                             marker='o', label='RMSE_test')
            if mean_:
                _ = plt.plot(self.x_split_range, [value['test_score'][1] for key, value in self.score_dict.items()],
                             marker='o', label='MEAN_test')
            # Test qui marche mais foireux avec le 0...
            if len(self.score_dict[0]['test_score']) > 2:
                _ = plt.plot(self.x_split_range, [value['test_score'][2] for key, value in self.score_dict.items()],
                             marker='o', label='MASE_test')

        if train:
            if rmse_:
                _ = plt.plot(self.x_split_range, [value['train_score'][0] for key, value in self.score_dict.items()],
                             marker='o', label='RMSE_train')
            if mean_:
                _ = plt.plot(self.x_split_range, [value['train_score'][1] for key, value in self.score_dict.items()],
                             marker='o', label='MEAN_train')
            # Test qui marche mais foireux avec le 0...
            if len(self.score_dict[0]['test_score']) > 2:
                _ = plt.plot(self.x_split_range, [value['train_score'][2] for key, value in self.score_dict.items()],
                             marker='o', label='MASE_train')

        _ = plt.xlabel('Nombre de lignes d\'apprentissage')
        _ = plt.ylabel('Valeur de l\'erreur')
        _ = plt.title('Erreur en CV Time Series')
        _ = plt.legend()
        _ = plt.show()

    def displayMeanMetrics(self, mase_=True, cut=4):
        print('RMSE MOYEN :',
              np.round(np.mean([value['test_score'][0] for key, value in self.score_dict.items()]), cut))
        print('MEAN MOYEN :',
              np.round(np.mean([value['test_score'][1] for key, value in self.score_dict.items()]), cut))
        if mase_:
            print('MASE MOYEN :',
                  np.round(np.mean([value['test_score'][2] for key, value in self.score_dict.items()]), cut))

    def getMeanMetrics(self, mase_=True, cut=4):
        rmse = np.round(np.mean([value['test_score'][0] for key, value in self.score_dict.items()]), cut)
        mean = np.round(np.mean([value['test_score'][1] for key, value in self.score_dict.items()]), cut)
        if mase_:
            mase = np.round(np.mean([value['test_score'][2] for key, value in self.score_dict.items()]), cut)
            return rmse, mean, mase
        return rmse, mean

    def createModelPredic(self, return_new=False):

        new_df = self.data['X'].copy()
        index_name = new_df.index.name

        new_df['_model_'] = -1
        new_df['_datetime_'] = new_df.index
        new_df = new_df.reset_index(drop=True)

        self.verbose('Création de la colonne _model_', 1)
        c = 0
        last = 0
        for i in range(len(self.x_split_range)):
            first, last = last, self.x_split_range[i]
            new_df.loc[(new_df.index >= first) & (new_df.index <= last), '_model_'] = c
            c += 1

        self.verbose('Création de la colonne _predic_', 1)
        new_df.loc[new_df['_model_'] == -1, '_model_'] = c
        new_df.set_index('_datetime_', inplace=True)
        new_df.index.name = index_name
        for i in new_df['_model_'].unique():
            if i > 0:
                new_df.loc[(new_df['_model_'] == i), '_predic_'] = self.score_dict[i - 1]['regr'].predict(
                    self.data['X'].copy().loc[new_df['_model_'] == i])

        self.data['predict_by_model'] = new_df[['_model_', '_predic_']]
        if return_new:
            return new_df

    def plotPredictions(self, nb=-1, y=True):
        if (nb not in self.score_dict.keys()) and nb != -1:
            max_ = max(self.score_dict.keys())
            print('No model named {}. Max is {}'.format(nb, max_))

        new_df = pd.concat([self.data['X'], self.data['predict_by_model']], axis=1)
        new_df['_target_'] = self.data['y']
        new_df['_datetime_'] = new_df.index
        _ = plt.subplots(figsize=(20, 5))

        # Plotting all models results per chunk
        if nb == -1:
            for i in new_df['_model_'].unique():
                if i != -1:
                    abscisses = new_df[new_df['_model_'] == i]['_datetime_']
                    ordonnees = new_df[new_df['_model_'] == i]['_predic_']
                    _ = plt.plot(abscisses, ordonnees, label=i)
                    _ = plt.title('Results of all CV-models')

        # Plotting results of one model on all data
        else:
            # Maybe use the predict function 
            mid_index = self.x_split_range[nb]
            regressor = copy.deepcopy(self.score_dict[nb]['regr'])
            time_value = new_df['_datetime_']
            to_predict = self.data['X'].copy()
            predicted_value = regressor.predict(to_predict)

            _ = plt.plot(time_value, predicted_value, label='test')
            _ = plt.plot(time_value.iloc[:mid_index], predicted_value[:mid_index], label='train')
            _ = plt.title('Model {}'.format(nb))

        if y:
            _ = plt.plot(new_df['_datetime_'], new_df['_target_'], c='grey', alpha=0.3)

        # Finally add ledeng to the plot
        _ = plt.legend()
        # if nb!=-1:
        #    return self.score_dict[nb]

    def getYValues(self, nb_model):

        # Prediction values
        y_pred_train = self.score_dict[nb_model]['y_pred_train']
        y_pred_test = self.score_dict[nb_model]['y_pred_test']

        # Real values
        y = self.data['y']
        mid_index = self.x_split_range[nb_model]
        y_train = y.iloc[:mid_index]
        y_test = y.iloc[mid_index:mid_index + len(y_pred_test)]

        return y_train, y_test, y_pred_train, y_pred_test

    def getXValues(self, nb_model):
        X = self.data['X']
        mid_index = self.x_split_range[nb_model]
        end_index = mid_index + len(self.score_dict[nb_model]['y_pred_test'])
        X_train = X.iloc[:mid_index]
        X_test = X.iloc[mid_index:end_index]
        return X_train, X_test

    def getOriginalData(self):
        X = self.data['X']
        y = self.data['y']
        return X, y

    def saveObject(self):
        result = {'title': self.title,
                  'nb_split': self.split_number,
                  'score_dict': self.score_dict,
                  'x_split_range': self.x_split_range}
        return result

    def restaure_from_dict(self, result, X, y):
        self.data['X'] = X
        self.data['y'] = y
        self.title = result['title']
        self.split_number = result['nb_split']
        self.score_dict = result['score_dict']
        self.x_split_range = result['x_split_range']
        self.initSplit(self.split_number)
        self.createModelPredic()
