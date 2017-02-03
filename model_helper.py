from sklearn.externals import joblib
import glob
import os
from time import strftime, gmtime

models_dir = os.path.join(os.path.dirname(__file__), 'models')
metrics_dir = os.path.join(models_dir, 'metrics')


def load_model(filename='', fast=True):
    if filename == '':
        filename_model = max(glob.iglob(os.path.join(models_dir, '*.jlb')), key=os.path.getctime)
        filename_metrics = os.path.join(metrics_dir, os.path.basename(filename_model))
    else:
        filename_model = os.path.join(models_dir, filename)
        filename_metrics = os.path.join(models_dir, filename)
    print 'read from file: ' + filename_model

    mae, r2, features, size = joblib.load(filename_metrics)
    if fast:
        return mae, r2, features, size
    else:
        model = joblib.load(filename_model)
        return model, mae, r2, features, size


def save_model(model, mae, r2, features, size):
    now = strftime("%Y-%m-%d_%H:%M:%S", gmtime())
    filename = 'm_' + now + '.jlb'
    _ = joblib.dump(model, os.path.join(models_dir, filename), compress=9)
    _ = joblib.dump((mae, r2, features, size), os.path.join(metrics_dir, filename), compress=9)
    print 'save to file: ' + filename
    return
