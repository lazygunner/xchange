# -*- coding:utf-8 -*-

from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)
from flask import render_template
app.config.from_pyfile('xchange.cfg', silent=True)
mongo = MongoClient(app.config['MONGO_HOST'], app.config['MONGO_PORT'])


@app.route('/')
def xchange():
    rate_dict = {}
    for item in app.config['ITEM_LIST']:
        id = item['id']
        rate = mongo.xchange.xchange.find({'item_id': id}).sort('time', -1)[0]
        rate_dict[id] = rate

    return render_template('index.html', rate_dict=rate_dict)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
