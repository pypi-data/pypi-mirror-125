# -*- coding: utf-8 -*-

#################################################################################
###                                                                           ###
###                                                                           ###
###                                     GENERAL                               ###
###                                                                           ###
###                                                                           ###
#################################################################################


# Making all necessary python imports for library use
import os as __os
import scipy as __sp
import numpy as __np
import math as __math
import json as __json
import pandas as __pd
import pickle as __pickle
import string as __string
import logging as __logging
import datetime as __datetime
import requests as __requests
import configparser as __configparser
import logger as __logger
from IPython.core.display import display, HTML

# Making local imports
# import time_format as t

# This is to avoid unuseful python warning with pandas
__pd.options.mode.chained_assignment = None

""""
#################################################################################
List of functions : 

 - (i) line
 - (i) parse_json
 - (i) url_to_json
 - (i) write_to_json_file
 - (i) read_file
 - (i) get_time_range_info_from_df
 - (i) save_df_to_excel
 - (i) transfoCol
 - (i) renameDfCol
 - (i) getPctValue
 - (i) star_print
 - (i) get_functions_in_file
 - (i) spacify_number

Indicators of importance :

(i)    : Important functions
(ii)   : Intermediary used functions
(iii)  : Not really used
(iii) !: To be deleted
 
#################################################################################
"""


def line(display=False):
    """To make easy separations while printing in console"""
    if display == True:
        return print("____________________________________________________________\n")



def num_to_str(num):
    """Function to convert a float to a string in dataframe
    (Used for dataframe => Might be deleted from this file"""
    return str(num)


def flatten_json(nested_json):
    """
        Flatten json object with nested keys into a single level.
        Args:
            nested_json: A nested json object.
        Returns:
            The flattened json object if successful, None otherwise.
    """
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(nested_json)
    return out

# def get_time_range_info_from_df(df, display=True, datetime_col=None):
#     if not datetime_col:
#         start = str(df.index[0])
#         end = str(df.index[-1])
#     else:
#         start = str(df[datetime_col].iloc[0])
#         end = str(df[datetime_col].iloc[-1])
#     if display:
#         print('Start : ', start, '\t', t.format_to_numeric_timestamp(start))
#         print('End   : ', end, '\t', t.format_to_numeric_timestamp(end))
#     return start, end


def save_df_to_excel(df, name='my_df_file.xlsx', open_=False):
    """This functions takes a dataFrame or list od dataFrames ans save it into an excel with one or multiple sheets.
    Parameters : df (dataframe to be saved), name (the name of the excel file with .xlsx at the end of it)
    """

    # If df is a single dataFrame : saving it into a classic excel file with one sheet
    if type(df) == __pd.core.frame.DataFrame:
        try:
            df.to_excel(name)
            print('File : ' + str(name) + ' has correctly been saved in the current folder')
            if open_:
                cmd_ = 'start excel.exe ' + name
                __os.system(cmd_)
        except:
            print('File : ' + str(name) + ' couldn\'t be saved. Might be open. Re-try.')
            # Check errors : could be because xlsx was not added

    # If df is a list of dataFrames : saving each of them in a sheet
    elif type(df) == list:
        list_df = df
        try:
            writer = __pd.ExcelWriter(name)
            compteur = 0
            for i in list_df:
                if len(i) == 1:
                    i[1].to_excel(writer, "Sheet_" + compteur)
                    compteur += 1
                if len(i) == 2:
                    i[1].to_excel(writer, i[0])
            writer.save()
            print('File : ' + str(name) + ' has correctly been saved in the current folder as a list of dataFrames')
        except:
            print('File : ' + str(name) + ' couldn\'t be saved as a list of dataFrames. Might be open. Re-try.')
            # Check errors : could be because xlsx was not added

    # If df is not one of the two defined formats => Error
    else:
        print('File send was not a dataFrame neither')
        # Add an assertion error ?



def transfo_col(ancien, ponctuation=None, accent=None, replacer='_'):
    """Description :
        simplifie une chaine de caractère en supprimant les majuscules, la ponctuation, les accents et les espaces
    inputs :
        - ancien as string : chaine à modifier
        - ponctuation as list : liste des caractères à retirer
        - accent as dict : dictionnaire des caractères à modifier par un autre
    outputs:
        - string : chaine de caractère modifiée (simplifiée)
    """

    if not ponctuation:
        caracters_to_remove = list(__string.punctuation) + [' ', '°']
        ponctuation = {initial: replacer for initial in caracters_to_remove}

    if not accent:
        avec_accent = ['é', 'è', 'ê', 'à', 'ù', 'ç', 'ô', 'î', 'â']
        sans_accent = ['e', 'e', 'e', 'a', 'u', 'c', 'o', 'i', 'a']
        accent = {sans: avec for sans, avec in zip(avec_accent, sans_accent)}

    ancien = str(ancien)
    ancien = ancien.lower()
    ancien = ancien.translate(str.maketrans(ponctuation))
    ancien = ancien.translate(str.maketrans(accent))
    double_replacer = replacer + replacer
    while double_replacer in ancien:
        ancien = ancien.replace(double_replacer, replacer)

    if ancien[0] == replacer:
        ancien = ancien[1:]

    if ancien[-1] == replacer:
        ancien = ancien[:-1]

    return ancien


def rename_df_col(df, replacer='_'):
    """Description : uniformise le nom des colonnes d'un dataframe en retirant les caractères spéciaux/surabondants
    inputs :
        - df as dataFrame : tableau de données dont les colonnes sont à renommer de manière plus simple
    outputs:
        - dataFrame : tableau de données dont les noms de colonnes ont été modifiés
    """
    rename_dict = {ancien: transfo_col(ancien, replacer=replacer) for ancien in df.columns}
    df_new = df.rename(columns=rename_dict)
    return df_new


def get_pct_value(value_, text_=False):
    pct = __np.round(value_ * 100, 2)
    if text_:
        return '{} %'.format(pct)
    return pct


def star_print(text, stars=10, length=None, symbol='*'):
    """Affichage d'une ligne avec une valeur au milieu
    Nécessite un texte, variable text as string
    Choix du nombre de caractères, variable length as int
    Choix du nombre d'étoiles avant/après le texte, variable stars as int
    Choix du symbole, variable symbol as string
    """
    if not length:
        return print(symbol * stars, text, symbol * stars)

    text_len = len(text)
    if text_len > length:
        return print(symbol * stars, text, symbol * stars)

    stars_start = ((length - text_len) / 2) - 1
    if stars_start == int(stars_start):
        return print(symbol * int(stars_start) + ' ' + text + ' ' + symbol * int(stars_start))
    else:
        stars_start = int(stars_start)
        return print(symbol * stars_start + ' ' + text + ' ' + symbol * (stars_start + 1))


def get_functions_in_file(file_name, print_=False):
    my_file = read_file(file_name=file_name)
    sp = my_file.split('\n')
    def_line = [i[4:].split('(')[0] for i in sp if i[:3] == 'def']

    if print_:
        print('List of functions')
        for i in def_line:
            print(' - {}'.format(i))
    return def_line


def get_categorical(df, verbose=False):
    cat_data = df.select_dtypes(include='object')
    num_data = df.select_dtypes(exclude='object')

    cat_cols = cat_data.columns.values
    num_cols = num_data.columns.values

    if verbose:
        print('\nCategorical Columns :\n ', cat_cols)
        print('\nNumerical Columns : \n', num_cols)
    return cat_cols, num_cols


def get_pct_empty_df(df):
    return __pd.DataFrame({'Emptiness (%)': __np.round((df.isnull().sum() / df.shape[0]) * 100)})


def return_middle_date(date1, date2):
    if date1 > date2:
        new_date = date2 + (date1 - date2) / 2
    else:
        new_date = date1 + (date2 - date1) / 2
    return new_date


def display_html(rep):
    display(HTML(rep.text))


def get_config(config_path):
    config = __configparser.ConfigParser()
    config.read(config_path)
    return config


def millify(n):
    n = float(n)
    millnames = ["", " K", " M", " B", " T"]
    millidx = max(0, min(len(millnames) - 1, int(__math.floor(0 if n == 0 else __math.log10(abs(n)) / 3))), )
    return "{:.0f}{}".format(n / 10 ** (3 * millidx), millnames[millidx])


def read_jl_file(file_name):
    values = []
    with open(file_name, 'rb') as file:
        line_ = 'line'
        while len(line_) > 1:
            line_ = file.readline()
            values.append(line_)
    values = values[:-1]
    values = [__json.loads(i) for i in values]
    df = __pd.DataFrame(values)
    return df


def save_ts_analyse():
    ts = str(__datetime.datetime.now())[:19]
    with open('data/last_analyse.txt', 'w') as file:
        file.write(ts)


def load_ts_analyse():
    with open('data/last_analyse.txt', 'r') as file:
        ts = file.read()
    ts = __pd.to_datetime(ts)
    return ts


def get_now():
    return str(__datetime.datetime.now())[:19].replace(' ', '_').replace(':', '-')


def define_logger():
    """ Example of use :
    logger = f.define_logger()
    logger.info('Start')
    """
    # create logger
    logger = __logging.getLogger('log')
    logger.setLevel(__logging.DEBUG)

    # create console handler and set level to debug
    ch = __logging.StreamHandler()
    ch.setLevel(__logging.DEBUG)

    # create formatter
    formatter = __logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)
    return logger


def timer(start_time=None):
    if not start_time:
        start_time = __datetime.datetime.now()
        return start_time
    elif start_time:
        thour, temp_sec = divmod((__datetime.datetime.now() - start_time).total_seconds(), 3600)
        tmin, tsec = divmod(temp_sec, 60)
        if thour < 1:
            print('\n Time taken: %i minutes and %s seconds.' % (tmin, round(tsec, 2)))
        else:
            print('\n Time taken: %i hours %i minutes and %s seconds.' % (thour, tmin, round(tsec, 2)))


# source https://www.kaggle.com/krishonaveen/xtreme-boost-and-feature-engineering
def reduce_mem_usage(df, verbose=True):
    numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
    start_mem = df.memory_usage().sum() / 1024 ** 2
    for col in df.columns:
        col_type = df[col].dtypes
        if col_type in numerics:
            c_min = df[col].min()
            c_max = df[col].max()
            if str(col_type)[:3] == 'int':
                if c_min > __np.iinfo(__np.int8).min and c_max < __np.iinfo(__np.int8).max:
                    df[col] = df[col].astype(__np.int8)
                elif c_min > __np.iinfo(__np.int16).min and c_max < __np.iinfo(__np.int16).max:
                    df[col] = df[col].astype(__np.int16)
                elif c_min > __np.iinfo(__np.int32).min and c_max < __np.iinfo(__np.int32).max:
                    df[col] = df[col].astype(__np.int32)
                elif c_min > __np.iinfo(__np.int64).min and c_max < __np.iinfo(__np.int64).max:
                    df[col] = df[col].astype(__np.int64)
            else:
                if c_min > __np.finfo(__np.float16).min and c_max < __np.finfo(__np.float16).max:
                    df[col] = df[col].astype(__np.float16)
                elif c_min > __np.finfo(__np.float32).min and c_max < __np.finfo(__np.float32).max:
                    df[col] = df[col].astype(__np.float32)
                else:
                    df[col] = df[col].astype(__np.float64)
    end_mem = df.memory_usage().sum() / 1024 ** 2

    if verbose:
        print('Mem. usage decreased to {:5.2f} Mb ({:.1f}% reduction) - From {} Mo to {} Mo.'.format(
            end_mem,
            100 * (start_mem - end_mem) / start_mem,
            __np.round(start_mem, 2),
            __np.round(end_mem, 2))
        )
    return df


def resumetable(df):
    print(f"Dataset Shape: {df.shape}")
    summary = __pd.DataFrame(df.dtypes, columns=['dtypes'])
    summary = summary.reset_index()
    summary['Name'] = summary['index']
    summary = summary[['Name', 'dtypes']]
    summary['Missing'] = df.isnull().sum().values
    summary['Uniques'] = df.nunique().values
    summary['First Value'] = df.loc[0].values
    summary['Second Value'] = df.loc[1].values
    summary['Third Value'] = df.loc[2].values

    for name in summary['Name'].value_counts().index:
        summary.loc[summary['Name'] == name, 'Entropy'] = round(
            __sp.stats.entropy(df[name].value_counts(normalize=True), base=2), 2)

    return summary


def split_ID_number(df, nb_split=7):
    for i in range(nb_split):
        df['TransactionID_{}'.format(i)] = df['TransactionID'].apply(lambda x: int(str(x)[i]))
    return df


def create_from_dt(df, col_name='TransactionDT'):
    dt = __pd.DataFrame(__pd.to_timedelta(df[col_name] * 1000000000))
    decomp = dt[col_name].dt.components[['days', 'hours', 'minutes']]
    decomp['days'] = decomp['days'] % 7
    decomp.columns = ['{}_{}'.format(col_name, i) for i in decomp.columns]
    return __pd.concat([df, decomp], axis=1)


def get_pct_empty_df(df):
    return __pd.DataFrame({'Emptiness (%)': __np.round((df.isnull().sum() / df.shape[0]) * 100)})


def fill_cat_nan(df, col_name, fill_with='NA', return_df=True):
    tmp = df[col_name].apply(lambda x: fill_with if __pd.isnull(x) else x)
    if not return_df:
        return tmp
    df[col_name] = tmp
    # Exploiter une boucle for pour faie un fill_categorical sur un ensemble de colonnes
    return df


# Filling numerical with median
def fill_num_nan(df, cols):
    if type(cols) == str:
        cols = [cols]
    df_local = df.copy()
    for col in cols:
        fill_value = df[col].median()
        df_local[col].fillna(fill_value, inplace=True)  # fill with median because mean may be affect by outliers.
    return df_local


# Cleaning infinite values to NaN
def clean_inf_nan(df):
    """Useful after numpy calculation errors to remove infinite values
    """
    return df.replace([__np.inf, -__np.inf], __np.nan)  # replace all nan,inf,-inf to nan so it will be easy to replace


def get_dum(df, col_name, del_col=True, drop_first=True):
    dum = __pd.get_dummies(df[col_name], drop_first=drop_first)
    if del_col:
        df = df.drop([col_name], axis=1)
    dum.columns = ['{}_{}'.format(col_name, i) for i in dum.columns]
    df = __pd.concat([df, dum], axis=1)
    return df


def get_nb_post_point(x):
    if not '.' in str(x):
        return 0
    e = str(x).split('.')
    # if len(e[-1])>5:
    #    print(e)
    if e[-1] == '0':
        return 0
    return len(e[-1])


def get_nb_pre_point(x):
    e = str(x).split('.')
    if e[0] == '0':
        return 0
    return len(e[0])


def get_number_around_point(df, col_name):
    df['{}_pre'.format(col_name)] = df[col_name].apply(get_nb_pre_point)
    df['{}_post'.format(col_name)] = df[col_name].apply(get_nb_post_point)
    return df


def calculation_from_amount(df):
    df['TransactionAmt_squared'] = df['TransactionAmt'] ** 2
    df['TransactionAmt_log'] = __np.log(df['TransactionAmt'])
    return df


def label_encoding(df, cols, verbose=False, get_encoders=False):
    """
    """
    local_df = df.copy()

    # Checking if one columns or more
    if type(cols) == str:
        if verbose: print('There is only one column : {}'.format(cols))
        cols = [cols]

    # Encoding categorical values
    encoders = {}
    for col in cols:
        nb_unique = local_df[col].nunique()
        print("Label encoding {} with {} unique values".format(col, nb_unique))
        if local_df[col].dtype == 'object':
            local_df[col], encoders[col] = encode_serie(local_df[col])
        else:
            print('Error : {} is not categorical'.format(col))
    if get_encoders:
        return local_df, encoders
    return local_df


def spacify_number(number):
    """ Takes a number and returns a string with spaces every 3 numbers
    """
    nb_rev = str(number)[::-1]
    new_chain = ''
    for val, letter in enumerate(nb_rev):
        if val%3==0:
            new_chain += ' '
        new_chain += letter
    final_chain = new_chain[::-1]
    return final_chain


class log_wrapped_function(object):
    def __init__(self, function):
        self.function = function

    def log_and_call(self, *arguments, **namedArguments):
        __logger.info('>>> Function {}'.format(self.function.__name__))
        local = locals()
        if 'arguments' in local.keys():
            __logger.debug('- arguments      : {}'.format(local['arguments']))
        if 'namedArguments' in local.keys():
            __logger.debug('- namedArguments : {}'.format(local['namedArguments']))
        self.function.__call__(*arguments, **namedArguments)

def print_parameters(function):
    return log_wrapped_function(function).log_and_call


def list_path(path):
    # https://stackoverflow.com/questions/9727673/list-directory-tree-structure-in-python
    pass

if __name__ == "__main__":
    print("All functions have been loaded.")
    _ = get_functions_in_file('general.py', print_=True)
