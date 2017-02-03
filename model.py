# -*- coding: utf-8 -*-
import pandas
from sklearn.ensemble import RandomForestRegressor
from sklearn import cross_validation
from sklearn.metrics import mean_absolute_error, r2_score
import model_helper

# model_helper.load_model()
data = pandas.read_csv('data.csv')

# print data

y = data['drive']
X = data.drop(['drive', 'data_from', 'data_add', 'url'], axis=1)

X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.25)

model = RandomForestRegressor(n_estimators=100)

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
names_feature = list(X.columns.values)
f_i_zipped = zip(names_feature, feature_importance.tolist())
f_i_zipped.sort(key=lambda t: t[1], reverse=True)
print 'Влияние факторов [top 10], %:'
for n, f in f_i_zipped:
    print " %10f - %s" % (f, n)
print '---' * 10
print ''

model_helper.save_model(fit, mae, r2, f_i_zipped, len(data))
