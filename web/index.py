# -*- coding: utf-8 -*-
from bottle import route, run, template, static_file



@route('/hello/<name>')
def test(name):
    return template('<b>Hello {{name}}</b>!', name=name)

@route('/')
def index():
    return template('index', name='Формула драйва')

@route('/<filename:path>')
def bootstrap(filename):
    return static_file(filename, root='')

run(host='localhost', port=8080)
