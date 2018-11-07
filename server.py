import json
import pymongo
import requests
import datetime

from flask import Flask, request, jsonify, abort, make_response
from pymongo import MongoClient

#create an instance of Flask (this is actually what is running the summer)
app = Flask(__name__)

#create client to run mongodb instanc (connects to default ost and port)
client = MongoClient()

#create database, but database not actually created until something inserted into items
db = client.database

entries = db.entries

#simple route to ensure that we can get connection between arduino and server
@app.route("/", methods=['GET'])
def hello():
    if request.method == 'GET':
        print('Hello there')
    else:
        print('Hello from no request')
    return "Hello There!", 200


#route for sensor 1 data
@app.route('/sensor1', methods=['POST','GET'])
def sensor1():
	if request.method == 'POST':
		entries.update_one({'sensorID':'sensor1'},
		{"$set": {'sensorID':request.json.get('sensor1'),
		'quatI':request.json.get('quatI'),
		'quatJ':request.json.get('quatJ'),
		'quatK':request.json.get('quatK'),
		'quatReal':request.json.get('quatReal'),
		'timestamp':str(datetime.datetime.now().time())}},
		upsert=True)
		return 'Data updated', 200
	elif request.method == 'GET':
		entry = entries.find_one({'sensorID':'sensor1'})
		result = {'sensorID':entry['sensorID'],'quatI':entry['quatI'],'quatJ':entry['quatJ'],
		'quatK':entry['quatK'],'quatReal':entry['quatReal'],'timestamp':entry['timestamp']}
		resp = make_response(jsonify(result), 200)
		return resp
	else:
		return 'Bad request', 400

#route for sensor 2 data
@app.route('/sensor2', methods=['POST','GET'])
def sensor2():
	if request.method == 'POST':
		entries.update_one({'sensorID':'sensor2'},
		{"$set": {'sensorID':request.json.get('sensor2'),
		'quatI':request.json.get('quatI'),
		'quatJ':request.json.get('quatJ'),
		'quatK':request.json.get('quatK'),
		'quatReal':request.json.get('quatReal'),
		'timestamp':str(datetime.datetime.now().time())}},
		upsert=True)
		return 'Data updated', 200
	elif request.method == 'GET':
		entry = entries.find_one({'sensorID':'sensor2'})
		result = {'sensorID':entry['sensorID'],'quatI':entry['quatI'],'quatJ':entry['quatJ'],
		'quatK':entry['quatK'],'quatReal':entry['quatReal'],'timestamp':entry['timestamp']}
		resp = make_response(jsonify(result), 200)
		return resp
	else:
		return 'Bad request', 400


#handle an incorrect route if one is given (i.e. error checking)
@app.errorhandler(404)
def route_not_found(error):
	print('Route ', request.path, 'not found')
	return 'Route does not exist', 404

#main, actually runs the flask application
#threaded allows connections from many clients and debug prints out debug statements
if __name__ == '__main__':
	app.run(threaded=True,debug=True)