import time as __time
import datetime as __datetime
import numpy as __np


def format_to_numeric_timestamp(time_var):
    # print('Start time_conversion with : {0}, of type : {1}'.format(time_var, type(time_var)))
    # TRY TO DEAL WITH : <class 'pandas._libs.tslib.Timestamp'>
    # #(when a date in a panda index) - use str() on it otherwise
    if type(time_var) == __datetime.datetime:
        time_var = str(time_var)

    if type(time_var) == float or type(time_var) == int:
        # print('Float or int : almost the good format')
        if time_var > 10000000000:
            # print('timestamp sent in microseconds : converted in miliseconds')
            return time_var / 1000
        # print('timestamp sent in milisenconds : OK')
        return time_var

    elif type(time_var) == str:
        format_1 = '%Y-%m-%d %H:%M:%S'
        format_2 = "%Y-%m-%dT%H:%M:%S.%f%z"
        format_3 = "%Y-%m-%dT%H:%M:%S.%fZ"
        format_4 = "%Y-%m-%dT%H:%M:%S.%f+0000"
        format_5 = "%Y-%m-%dT%H:%M:%S.%f+0000"
        format_6 = "%Y-%m-%dT%H:%M:%S"

        for time_format in [format_1, format_2, format_3, format_4, format_5, format_6]:
            try:
                # numeric_timestamp = time.strftime(time_format,time.gmtime(time_var))
                numeric_timestamp = __time.mktime(__datetime.datetime.strptime(time_var, time_format).timetuple())
                # print('String corresponds to format : {}'.format(time_format))
                return int(numeric_timestamp)
            except:
                # print('String : {1} doesn\'t match with format {0}'.format(time_format, time_var))
                pass
        # print('String sent : {} doesn\'t match with any registered format'.format(time_var))

        return time_var

    else:
        print('Type of time variable, is not a string neither a float or int, but {}'.format(type(time_var)))
        print('Thus conversion was not realized, return : {}'.format(time_var))
        return time_var


def format_to_df_time(format_):
    """Takes any format of date and transform it to dataFrame timestamp format : %Y-%m-%d %H:%M:%S"""
    if not format_:
        return None
    if format_ == __np.NaN:
        return None
    numeric_timestamp = format_to_numeric_timestamp(format_)
    dt = __datetime.datetime.utcfromtimestamp(numeric_timestamp)
    string = dt.strftime('%Y-%m-%d %H:%M:%S')
    return string


def format_to_date_time(format_, as_string=False):
    """Takes any format of date and transform it to datetime format.
    Arg : as_string : set to true, transfroms it into a classic human readable format"""
    if not format_:
        return None
    numeric_timestamp = format_to_numeric_timestamp(format_)
    datetime_ts = __datetime.datetime.utcfromtimestamp(numeric_timestamp)
    if as_string:
        return str(datetime_ts)
    return datetime_ts


def format_to_cloud_string(format_):
    """Takes any format of date and transform it to cloud timestamp format : %Y-%m-%dT%H:%M:%S.000Z"""
    if not format_:
        return None
    numeric_timestamp = format_to_numeric_timestamp(format_)
    dt = __datetime.datetime.utcfromtimestamp(numeric_timestamp)
    string = dt.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    return string


def time_between_two_dates(start, end):
    start_datetime = format_to_date_time(start)
    end_datetime = format_to_date_time(end)

    nb_days = end_datetime - start_datetime
    nb_days_str = str(nb_days)

    return nb_days_str


def current_time_string():
    """Description : renvoie l'heure actuelle UTC au format AAAAMMJJ_HHMMSS 
    inputs :
        - None
    outputs:
        - string : heure au format indiqué ci-dessus
    """
    return str(__datetime.datetime.now()).replace(' ', '_').replace(':', '').replace('-', '')[:15]
