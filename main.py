# -*- coding: utf-8 -*-
import requests
import pandas
import lxml.html as lh
from time import gmtime, strftime, time, sleep
import os.path

batch = 1000
filename = 'data.csv'

nodes = {
    'likes': '.c-like__counter',
    'drive': '.c-car-info__nums > span > strong',
    'followers': '#car-followers',
    'bj': '.c-car-info__nums > a:last-child > strong',
    'comments': '#commentstitle > span',
    'bj_likes': '.c-lb-card > .c-lb-card__likes > a',
    'bj_comments': '.c-lb-card > .c-lb-card__comments > a',
    'data_from': '.c-car-ministats > span'
}


df = pandas.DataFrame(columns=(sorted(nodes.keys()) + ['url', 'data_add']))

time_prof = []
i = 0

while True:
    start = time()

    try:
        r = requests.get('https://www.drive2.ru/random/')
    except requests.exceptions.ConnectionError:
        print 'Connection refused, sleep 10s'
        sleep(500)
        continue

    doc = lh.fromstring(r.text)

    data = {}
    for key, val in nodes.items():
        try:
            data[key] = doc.cssselect(val)[0].text_content()
        except IndexError:
            data[key] = 0
        else:
            data[key] = doc.cssselect(val)[0].text_content()

        if key == 'bj_likes' or key == 'bj_comments':
            data[key] = sum(int(str(a.text_content()).strip()) for a in doc.cssselect(val))

        if key == 'data_from':
            data[key] = doc.cssselect(val)[0].get('data-tt')

    # data['data_from'] = data['data_from'].encode()
    df.loc[i] = [data[key] for key in sorted(nodes.keys())] + [r.url, strftime("%Y-%m-%d %H:%M:%S", gmtime())]
    i += 1

    stop = time()
    time_prof.append(stop - start)

    if i >= batch:
        header_print = True
        if os.path.isfile(filename):
            header_print = False
        df.to_csv(filename, index=False, mode='a', encoding="utf-8", header=header_print)
        df = pandas.DataFrame(columns=sorted(nodes.keys()) + ['url', 'data_add'])
        i = 0
        print "save %s - %f s per one" % (batch, sum(time_prof) / batch)
        time_prof = []