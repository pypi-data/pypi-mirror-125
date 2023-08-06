import numpy as __np
import pandas as __pd
import ruptures as __rpt
import matplotlib.pyplot as __plt

from sklearn.preprocessing import LabelEncoder as __LabelEncoder


def create_roll(ser_, nb_roll=100):
    ser_ = ser_.rolling(nb_roll, min_periods=1).mean()
    min_ser = min(ser_)
    max_ser = max(ser_ * 1.3)
    return ser_, min_ser, max_ser


def iqr_detect_outlier(data):
    """
    Detect outliers in data given Boxplot rule:
        X is an outlier <=> X>q3+1.5*IQR or X<q1-1.5*IQR 
    Args:
        data (Array): list of values to check outliers
        
    """

    q1, q3 = __np.percentile(data, [25, 75])
    iqr = q3 - q1
    cut_off = iqr * 1.5
    lower_bound, upper_bound = q1 - cut_off, q3 + cut_off

    return data[(data <= lower_bound) | (data >= upper_bound)]


def zscore_detect_outlier(data):
    """
    Detect outliers in data given Zscore rule:
        X is an outlier <=> |X|>E(X)+3*S(X)
    Args:
        data (Array): list of values to check outliers
        
    """
    threshold = 3
    mean = __np.mean(data)
    std = __np.std(data)
    z_score = __np.abs((data - mean) / std)
    outliers_idx = z_score[z_score > threshold].index

    return data.iloc[outliers_idx]


def shift_detect(data, model="l2", width=40, noise_std=4, debug=False):
    """
    Shift detection using window based method (see gitlab wiki for more info)
    
    Args:
        data (Array)    : list of values to check outliers
        model (String)  : which distance to use
        width (int)     : Window width
        noise_std(float): std for estimated noise
        debug (Bool)    : to display shift in data
        
     Returns:
         List: shift starting points 
    """

    n = len(data)
    pen = __np.log(n) * noise_std ** 2
    algo = __rpt.Window(width=width, model=model).fit(data)
    shifts = algo.predict(pen=pen)

    if debug:
        __rpt.show.display(data, shifts, figsize=(10, 6))
        __plt.show()

    return shifts[:-1]


def get_normalized_serie(df, col):
    normalized = ((df[col] - df[col].min()) / (df[col].max() - df[col].min()) + 1)
    return normalized


def encode_serie(serie):
    lbl = __LabelEncoder()
    lbl.fit(serie.apply(str).values)
    serie = lbl.transform(list(serie.apply(str).values))  # Ajout du str (sinon fonctionne pas sur nombre)
    return serie, lbl


# /Users/thibaud/Documents/Python_scripts/02_Projects/SNCF/open_data/sncf_utils.py
def transform_category_to_color(df, col_name, colors=None):
    if colors is None:
        colors = ['red', 'blue', 'green', 'yellow', 'orange'] * 50
    ser = df[col_name]
    ser, _ = encode_serie(ser)
    ser = __pd.Series(ser).apply(lambda x: colors[int(x)])
    return ser


def min_max_date(df):
    min_date = df['Year'].min()
    max_date = df['Year'].max()
    if min_date > max_date:
        tmp = min_date
        min_date = max_date
        max_date = tmp
    return min_date, max_date


def get_dummy(df, col):
    """
    Transform a pandas Series into dummies col
    """
    ser_ = df[col]
    dummies_data = __pd.get_dummies(ser_, drop_first=False)
    dummies_data.columns = ['{}_{}'.format(col, i) for i in dummies_data.columns]
    df = __pd.concat([df, dummies_data], axis=1)
    return df


def extract_car(df, col, car_number):
    """
    Extract one caracter of a pandas Series
    """
    new_col_name = '{}_{}'.format(col, str(car_number))
    ser_ = df[col].apply(str)
    df[new_col_name] = ser_.apply(lambda x: x[car_number])
    return df


def to_numeric_categorical(df, col):
    """
    Get a pandas Series and transforms every item into an integer value.
    """
    ser_ = df[col]
    unique_list = ser_.unique()
    nb = 0
    for i in unique_list:
        ser_ = ser_.apply(lambda x: x.replace(i, str(nb)))
        nb += 1
    df[col] = ser_
    return df


def get_categorical(df, verbose=False):
    cat_data = df.select_dtypes(include='object')
    num_data = df.select_dtypes(exclude='object')

    cat_cols = cat_data.columns.values
    num_cols = num_data.columns.values

    if verbose:
        print('\nCategorical Columns :\n ', cat_cols)
        print('\nNumerical Columns : \n', num_cols)
    return cat_cols, num_cols



def compute_variances(df, col, agg_col='ID_SEGMENT', round_=3):
    """
    About Variance https://bit.ly/3eM23Es
    - Variance inter : Variance of class's Average (variance résiduelle)
    - Variance intra : Weighted Average of class's Variances (variance expliquée)
    """

    # Variance
    var = np.var(df[col])
    var = round(var, round_)
    
    # Variance Inter
    var_inter = df.groupby(agg_col).agg({col:'mean'})
    var_inter = statistics.variance(var_inter[col])
    var_inter = round(var_inter, round_)
    
    # Variance Intra
    var_intra = df.groupby(agg_col).agg({col:[np.var, 'count']})
    var_intra.columns = ['var', 'count']
    var_intra['VAR_INTRA'] = (var_intra['count'] / var_intra['count'].sum()) * var_intra['var']
    var_intra = var_intra['VAR_INTRA'].round(round_).sum()

    return {
        'column':col,
        'var':var,
        'var_intra':var_intra,
        'var_inter':var_inter,
        'homogene':var_intra<var_inter
    }