# -*- coding:utf-8 -*-

from datetime import datetime, timedelta
import json

import requests
from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)
app.config.from_pyfile('xchange.cfg', silent=True)
mongo = MongoClient(app.config['MONGO_HOST'], app.config['MONGO_PORT'])


def get_xchange(api_url, item):
    url = api_url.format(item['id'])
    rsp = requests.get(url)
    data = json.loads(rsp.content)
    rate = data['query']['results']['rate']
    new_rate = parse_rate(rate)
    new_rate['name'] = item['name']
    return new_rate


def parse_rate(rate):
    date = datetime.strptime(rate['Date'], '%m/%d/%Y')

    origin_time = rate['Time'][:-2]
    hour, minute = origin_time.split(':')
    am = origin_time[-2:]
    if am == 'pm':
        hour += 12

    time = date + timedelta(hours=int(hour), minutes=int(minute))

    result = {
        'item_id': rate['id'],
        'rate': float(rate['Rate']),
        'time': time,
    }

    return result


def get_xchange_routine():
    for item in app.config['ITEM_LIST']:
        rate = get_xchange(app.config['API_URL'], item)
        mongo.xchange.xchange.update(
            {
                'item_id': rate['item_id'],
                'time': rate['time'],
            },
            rate,
            upsert=True
        )


if __name__ == '__main__':
    get_xchange_routine()

