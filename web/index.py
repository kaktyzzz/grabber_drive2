# -*- coding: utf-8 -*-
from bottle import route, run, template, static_file
import sys
import os
sys.path.insert(0, os.path.join(sys.path[0], '../'))

import model_helper

@route('/hello/<name>')
def test(name):
    return template('<b>Hello {{name}}</b>!', name=name)

@route('/')
def index():
    mae, r2, features, size = model_helper.load_model()
    weight = []
    summa = 0
    for n, v in features:
        weight.append('{:8.5f}'.format(v))
    for n, v in features[4:]:
        summa += v

    return template(
                    'index',
                    name='Формула рассчета драйва',
                    mae='{:5.2f}'.format(mae),
                    r2='{:5.2f}'.format(r2 * 100) + '%',
                    count='{:d}'.format(int(size/1000)) + ' K',
                    followers=weight[0],
                    bj_likes=weight[1],
                    likes=weight[2],
                    comments=weight[3],
                    other='{:8.5f}'.format(summa))

@route('/<filename:path>')
def bootstrap(filename):
    return static_file(filename, root='')

# run(host='localhost', port=8080)
