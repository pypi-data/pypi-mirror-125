import numpy as np
import pandas as pd


class PocotoTest():

    def __init__(self, env='dev'):
        self.name = 'Test'
        self.rapport = {}

    def set_name(self, name):
        self.name = name
        self.rapport[name] = {}

    def display_rapport(self):
        for key, value in self.rapport.items():
            print('\n')
            print('>', key)
            print(value)

    def check_missing_values(self, df):
        tmp = df.isnull().sum()
        tmp = tmp[tmp > 0].to_dict()

        print('\n> Checking missing values')
        for key, value in tmp.items():
            print('MISSING', value, '\t', key)
        if len(tmp.keys()) == 0:
            print('- No missing values')
            df['missing'] = None
        self.rapport[self.name]['missing'] = np.NaN
        return df

    def check_min_max_values(self, df, list_of_col):
        print('\n> Checking missing values')
        for col in list_of_col:
            print(col, '-' 'min :\t', df[col].min())
            print(col, '-' 'max :\t', df[col].max())
        return df

    def get_range(self, df, col='datetime'):
        return df[col].max() - df[col].min()

    def check_datetime_range(self, df):
        start = df.datetime.min()
        end = df.datetime.max()
        range_ = self.get_range(df)
        print('\n> Time information')
        print('START :\t', start)
        print('END   :\t', end)
        print('Total :\t', range_)
        return df

    def check_four_information(self, df):
        print('\n> Values per furnace')
        tmp = df['four'].value_counts().sort_index()
        for key, value in tmp.items():
            print('Four', '\t', key, '\t', value)
        return df

    def check_information(self, df, col='four', surname='Four'):
        print('\n> Values per {}'.format(surname))
        tmp = df[col].value_counts().sort_index()
        for key, value in tmp.items():
            print(surname, '\t', key, '\t', value)
        return df

    def check_four_information(self, df):
        return self.check_information(df, 'four', 'Four')

    def check_type_information(self, df):
        return self.check_information(df, 'type', 'Type')

    def check_face_information(self, df):
        return self.check_information(df, 'face', 'Face')

    def check_tag_information(self, df):
        range_ = self.get_range(df)
        
        # Checking Tag informations
        print('\n> Values per Tag')
        nb_tag = df['tag'].nunique()
        val_per_tag_real = df.groupby('tag').size().mean().round()
        val_per_tag_supo = np.round(range_ / pd.Timedelta('10min'), 0)
        pct_per_tag = np.round((val_per_tag_real / val_per_tag_supo) * 100, 2)
        print('Tags nb\t', nb_tag)
        print(val_per_tag_real, '\t(avg value per tag)')
        print(val_per_tag_supo, '\t(supposed value per tag)')
        print(pct_per_tag, '\t%')

        # Checking errors in description
        tmp = df.groupby('tag').nunique()['tag']
        tmp = tmp[tmp != 1]
        tmp = tmp[tmp > 0].to_dict()
        for key, value in tmp.items():
            print('TAG - ', key, '\t', value, 'different descriptions')
        return df

    def check_alerts(self, df):
        print('\n> Checking alerts')
        tmp = df['alert_num'].value_counts()
        for key, value in tmp.items():
            pct_value = np.round((value / df.shape[0]) * 100, 2)
            print('Alerts', '\t', key, '\t', pct_value, '%')
        return df

    def print_test(self):
        print('Test', self.name)
