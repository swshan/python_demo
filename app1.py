#coding=utf8

from flask import Flask, request, jsonify
import pymongo
from bson.json_util import dumps
import json

app = Flask(__name__)


def get_mongo(db_info='test'):

    myclient = pymongo.MongoClient(host='192.168.50.181:27017', connectTimeoutMS=2000)
    db = myclient[db_info]
    return db

def insert_mongo(db,data):
    collection = db['todos']
    if data is not None:
        post_id = collection.insert_one(data).inserted_id
    
    return post_id

def query_mongo(db):
    collection = db['todos']
    data = collection.find()
    return data

def bson_to_json(document_list):
    return json.dumps(json.loads(dumps(document_list)))

@app.route('/todo/', methods=['GET']) 
def query_all():
    db = get_mongo()
    items = query_mongo(db)
    return bson_to_json(items)

@app.route('/todo/api/add', methods=['GET','POST'])
def parse_request():
    data = request.json
    if data is None:
        return jsonify('400')
    db = get_mongo()
    inserted = insert_mongo(db, data)
    if not inserted:
        return jsonify('400')
    return json.dumps('200')

def main():
    app.run(debug=True,host='0.0.0.0')

main()

