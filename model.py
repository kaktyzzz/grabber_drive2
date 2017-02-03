# -*- coding: utf-8 -*-
import pandas
from sklearn.externals import joblib
import glob
import os
from time import strftime, gmtime
from sklearn.ensemble import RandomForestRegressor
from sklearn import cross_validation
from sklearn.metrics import mean_absolute_error, r2_score

models_dir = 'models'
metrics_dir = os.path.join(models_dir)


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

data = pandas.read_csv('data.csv')

# print data

y = data['drive']
X = data.drop(['drive', 'data_from', 'data_add', 'url'], axis=1)

X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.25)

model = RandomForestRegressor(n_estimators=2)

fit = model.fit(X_train, y_train)
predict = fit.predict(X_test)

# print 'drive true: '
# print y_test
# print 'drive pred: '
# print predict
mae = mean_absolute_error(y_test, predict)
r2 = r2_score(y_test, predict)

print 'abs_err: %f' % mae
print 'r2     : %f' % r2

feature_importance = model.feature_importances_
names_feature = list(X_train.columns.values)
f_i_zipped = zip(names_feature, feature_importance.tolist())
f_i_zipped.sort(key=lambda t: t[1], reverse=True)
print 'Влияние факторов [top 10], %:'
for n, f in f_i_zipped:
    print " %10f - %s" % (f, n)
print '---' * 10
print ''

save_model(fit, mae, r2, f_i_zipped, len(data))
mae, r2, features, size = load_model()
print size
