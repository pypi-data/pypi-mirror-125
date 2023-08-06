# Making all necessary python imports for library use
import random as __random
import numpy as __np
import pandas as __pd
from PIL import Image as __Image  # pip install pillow
# from statsmodels.tsa.stattools import adfuller


from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

"""
#################################################################################

List of functions :

 - create_clean_df_from_cloud_json
 - create_image
 - json_to_df
 - set_timestamp_df_index

#################################################################################
"""


def create_clean_df_from_cloud_json(js):
    """ Given a json downloaded on the cloud from get_datasource_data or get_location_data, returns a corrected df"""
    df = json_to_df(js)
    df_data = set_timestamp_df_index(df)
    for col in df_data.columns:
        if col[:6] == 'values':
            df_data[col] = __pd.to_numeric(df_data[col], errors='coerce')
    return df_data


def create_image():
    size = (256, 256)
    im = __Image.new('RGB', size)
    pix = im.load()
    for i in range(size[0]):
        for j in range(size[1]):
            pix[i, j] = (i, int(0.5 * i + __random.randint(0, 127)), int(0.5 * j + __random.randint(0, 127)))
    im.show()


def json_to_df(json_file, keys=False):
    """Description : Transforms data of a json to a pandas DataFrame
    Takes : json_file as list of dictionnaries
    Returns : A pandas dataFrame with all the datas converted in nice columns easy to deal with
    """
    try:
        # lists_initialization
        liste_keys = []
        new_list = []

        # still_dic is a variable which detects if there is still a deeper dictionnary into the current dictionnary
        still_dic = True
        compteur = 0

        # While there is a dictionnary we go down into it to get #order1 dictionnary
        while still_dic == True:
            # still_dic is set to false and if we find a dictionnary we'll set it back to True
            still_dic = False
            # json_file is the list of dictionnaries in the json_file : let's read it
            # We want to detect the dictionnaries odf deeper order and transform them into simple dictionnaries

            for bloc in json_file:
                new_dic = {}
                # print(bloc)
                for i in bloc.keys():
                    if type(bloc[i]) == dict:
                        for j in bloc[i].keys():
                            # renaming {key_1:{key_2:'bla'}} in {key_1_key_2:'bla'}
                            liste_keys.append(str(i) + '_' + str(j))
                            new_dic[str(i) + '_' + str(j)] = bloc[i][j]
                            if type(bloc[i][j]) == dict:
                                still_dic = True
                    else:
                        liste_keys.append(i)
                        new_dic[str(i)] = bloc[i]
                new_list.append(new_dic)
                # Once we have transformed dictionnaries in dictionaries to simple dictionnaries with more keys we remplace the json file
            # It will still have the same length

            json_file = new_list
            new_list = []
            compteur += 1

        # We now have a json file with n dictionnaries of order one (no dict in dict)
        # getting all its keys in alphabetical order
        liste_keys = list(set(liste_keys))
        liste_keys.sort()
        final = []

        # looping on the json_file we transform dict in columns and dataFrame
        for i in json_file:
            interm = []
            for elt in liste_keys:
                interm.append(i[elt]) if elt in i else interm.append('')
            final.append(interm)
        data_array = __np.array(final)
        df_data = __pd.DataFrame(data_array, columns=liste_keys)
        # print('Converting json file to df : End')

        if keys:
            return df_data, liste_keys
        else:
            return df_data
    except:
        print('Error : DataFrame couldn\'t be transformed from json')


def set_timestamp_df_index(df, column='timestamp', del_col=True):
    """used to transform dataFrame with cloud timestamp format (%Y-%m-%dT%H:%M:%S.000Z)
    into dataFrame with pandas timestamp index.
    del_col (true by default) : delete the column with the original timestamp format
    column : name of the column to deal with.
    Returns the corrected dataFrame"""
    init_df = df.copy()
    try:
        df[column] = __pd.to_numeric(df[column])
        df[column] = __pd.to_datetime(df[column].apply(t.format_to_df_time))
        df.index = df[column]
        if del_col:
            del (df[column])
        return df

    except:
        return init_df


# def test_stationarity(timeseries, window=12):
#     # Determing rolling statistics
#     rolmean = timeseries.rolling(window=window).mean()
#     rolstd = timeseries.rolling(window=window).std()

#     # Plot rolling statistics:
#     orig = plt.plot(timeseries, color='blue', label='Original')
#     mean = plt.plot(rolmean, color='red', label='Rolling Mean')
#     std = plt.plot(rolstd, color='black', label='Rolling Std')
#     plt.legend(loc='best')
#     plt.title('Rolling Mean & Standard Deviation')
#     plt.show(block=False)

#     # Perform Dickey-Fuller test:
#     print('Results of Dickey-Fuller Test:')
#     dftest = adfuller(timeseries, autolag='AIC')
#     dfoutput = pd.Series(dftest[0:4], index=['Test Statistic', 'p-value', '#Lags Used', 'Number of Observations Used'])
#     for key, value in dftest[4].items():
#         dfoutput['Critical Value (%s)' % key] = value
#     print(dfoutput)


def get_granularity(start_date, end_date):
    range_list = [(365, 'year'), (90, '3months'), (30, 'month'), (7, 'week'), (1, 'day')]

    diff_days = (end_date - start_date).days
    if diff_days < 0:
        return 'Error : start_date ({}) < end_date ({})'.format(start_date, end_date)
    for i in range_list:
        if diff_days >= i[0]:
            return i[1]
    return range_list[-1][1]


if __name__ == "__main__":
    print("All secundary functions have been loaded.")
