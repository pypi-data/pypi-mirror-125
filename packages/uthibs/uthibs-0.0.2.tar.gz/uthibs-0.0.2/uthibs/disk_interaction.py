import os
import json
import pickle
import requests


def parse_json(path):
    """Given a json_file =path loading it and sending a dictionary back"""
    with open(path) as f:
        data = json.load(f)
    return data


def url_to_json(url):
    """ Given a web url with a json file, returns a dictionary"""
    r = requests.get(url)
    json_file = r.json()
    return json_file


def save_json(file_name, data, path='./'):
    """Saving as a json file in one line"""
    file_path = path + file_name
    with open(file_path, 'w') as fp:
        json.dump(data, fp)


def read_file(file_name='data.txt'):
    """ Example of file name 'data.txt' """
    with open(file_name, "r") as fichier:
        file = fichier.read()
    return file


def get_token(path):
    with open(path, 'r') as file:
        api_key = file.read()
    return api_key


def load_pickle(file_name):
    PICKLE_PATH = parse_json('../src/params.json')['PICKLE_PATH']
    file_path = PICKLE_PATH + file_name
    with open(file_path, 'rb') as pfile:
        my_pickle = pickle.load(pfile)
    return my_pickle


def save_pickle(object_, file_name):
    PICKLE_PATH = parse_json('../src/params.json')['PICKLE_PATH']
    file_path = PICKLE_PATH + file_name
    with open(file_path, 'wb') as pfile:
        pickle.dump(object_, pfile, protocol=pickle.HIGHEST_PROTOCOL)


def list_pickle():
    PICKLE_PATH = parse_json('../src/params.json')['PICKLE_PATH']
    file_list = os.listdir(PICKLE_PATH)
    pickle_list = [i for i in file_list if '.p' in i]
    print(pickle_list)


# YAML
# import yaml
# import pathlib

# def load_config(config_filename):
#     with open(pathlib.Path(__file__).parent / config_filename) as stream:
#         data_loaded = yaml.safe_load(stream)
#     return data_loaded

# with open("drift_config.yaml", 'r') as stream:
#     data_loaded = yaml.safe_load(stream)

# print(data_loaded)

# error_limit:
#   MAPE_14H: 5
#   MAPE_15H: 10
#   MAPE_16H: 10
#   MAPE_17H: 10
#   MAPE_18H: 10
#   MAPE_19H: 10
#   MAPE_20H: 10
# avert_data:
#   nb_days_analyse: 7
#   nb_days_alert: 2
#   color: FFD700
#   titre: Dérive du modèle - Alerte
#   message: Le modèle commence à dériver, un ré-entrainement pourrait survenir prochainement
# retrain_data:
#   nb_days_analyse: 7
#   nb_days_alert: 14
#   color: 850606
#   titre: Dérive du modèle - Ré-entrainement
#   message: Le modèle dérive depuis 10 jours, un ré-entrainement vient d'être enclenché
# webhoook:
#   url: https://mousquetaires.webhook.office.com/webhookb2/a2e753ef-4c43-4ecc-a111-dde5c8767ed8@ebaeb74c-eeae-40f8-b755-10b0e2bf7528/IncomingWebhook/5c323e2b2e254db091e31464d032336e/49c2927e-6269-4317-9d68-d2d1057b07fb