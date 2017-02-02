# -*- coding: utf-8 -*-
import pandas
from sklearn.ensemble import RandomForestRegressor
from sklearn import cross_validation
from sklearn.metrics import mean_absolute_error, r2_score

data = pandas.read_csv('data.csv')

# print data

y = data['drive']
X = data.drop(['drive', 'data_from', 'data_add', 'url'], axis=1)

import sys, os, bottle
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import index # Основной файл

application = bottle.default_app()

X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.25)

model = RandomForestRegressor(n_estimators=200)

fit = model.fit(X_train, y_train)
predict = fit.predict(X_test)

print 'drive true: '
print y_test
print 'drive pred: '
print predict
print 'abs_err: %f' % mean_absolute_error(y_test, predict)
print 'r2     : %f' % r2_score(y_test, predict)

feature_importance = model.feature_importances_
names_feature = list(X_train.columns.values)
f_i_zipped = zip(names_feature, feature_importance.tolist())
f_i_zipped.sort(key=lambda t: t[1], reverse=True)
print 'Влияние факторов [top 10], %:'
for n, f in f_i_zipped:
    print " %10f - %s" % (f, n)
print '---' * 10
print ''


