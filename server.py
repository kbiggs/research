import json
import pymongo
import requests
import datetime
from datetime import timedelta

from flask import Flask, request, jsonify, abort, make_response
from pymongo import MongoClient
import csv

#create an instance of Flask (this is actually what is running the summer)
app = Flask(__name__)

#create client to run mongodb instanc (connects to default ost and port)
client = MongoClient()

#create database, but database not actually created until something inserted into items
dbase = client.database

entries = dbase.entries

timestamp = datetime.datetime.now().time()

filenames = ['sensorID', 'quatI', 'quatJ', 'quatK', 'quatReal', 'timestamp']
file = open('data.csv', 'w')

with file:
    writer = csv.DictWriter(file, fieldnames=filenames)
    writer.writeheader()
    
def writeToCSV(sensorID, quatI, quatJ, quatK, quatReal, timestamp):
    file = open('data.csv', 'a')
    with file:
        writer = csv.DictWriter(file, fieldnames=filenames)
        writer.writerow({'sensorID':sensorID,
            'quatI':quatI,
            'quatJ':quatJ,
            'quatK':quatK,
            'quatReal':quatReal,
            'timestamp':timestamp})

#simple route to ensure that we can get connection between arduino and server
@app.route("/", methods=['POST','GET'])
def hello():
    if request.method == 'GET':
        print('Hello there')
    elif request.method == 'POST':
        print('Hello from post')
    else:
        print('Hello from no request')
    return "Hello There!", 200


#route for sensor 1 data
@app.route('/sensor1', methods=['POST','GET'])
def sensor1():
        global timestamp
	if request.method == 'POST':
                #print(datetime.datetime.now().time())
                print(str(datetime.datetime.now().time()))
                timestamp = datetime.datetime.now().time()
                newTime = datetime.datetime(2019, 4, 11, timestamp.hour, timestamp.minute, timestamp.second, timestamp.microsecond)
                '''print('K: ', request.json.get('quatK'))
                print('I: ', request.json.get('quatI'))
                print('J: ', request.json.get('quatJ'))
                print('R: ', request.json.get('quatReal'))'''
                print(request.json.get('sensorID'))
                splitK = request.json.get('quatK').split(",")
                splitI = request.json.get('quatI').split(",")
                splitJ = request.json.get('quatJ').split(",")
                splitR = request.json.get('quatReal').split(",")
		entries.update_one({'sensorID':'sensor1'},
		{"$set": {'sensorID':request.json.get('sensorID'),
		'quatI':request.json.get('quatI'),
		'quatJ':request.json.get('quatJ'),
		'quatK':request.json.get('quatK'),
		'quatReal':request.json.get('quatReal'),
		'timestamp':str(datetime.datetime.now().time())}},
		upsert=True)
		for i in range(len(splitK)):
                    incTime = newTime + timedelta(microseconds=50000)
                    writeToCSV('sensor1',splitI[i],splitJ[i],splitK[i],splitR[i],str(incTime.time()))
                    newTime = datetime.datetime(2019, 4, 11, incTime.hour, incTime.minute, incTime.second, incTime.microsecond)
		return 'Data updated', 200
	elif request.method == 'GET':
		entry = entries.find_one({'sensorID':'sensor1'})
		print(entry)
		result = {'sensorID':entry['sensorID'],'quatI':entry['quatI'],'quatJ':entry['quatJ'],
		'quatK':entry['quatK'],'quatReal':entry['quatReal'],'timestamp':entry['timestamp']}
		resp = make_response(jsonify(result), 200)
		return resp
	else:
		print('in else')
		return 'Bad request', 400

#route for sensor 2 data
@app.route('/sensor2', methods=['POST','GET'])
def sensor2():
        global timestamp
	if request.method == 'POST':
                #print(datetime.datetime.now().time())
                print(str(datetime.datetime.now().time()))
                newTime = datetime.datetime(2019, 4, 11, timestamp.hour, timestamp.minute, timestamp.second, timestamp.microsecond)
                '''print('K: ', request.json.get('quatK'))
                print('I: ', request.json.get('quatI'))
                print('J: ', request.json.get('quatJ'))
                print('R: ', request.json.get('quatReal'))'''
                print(request.json.get('sensorID'))
                splitK = request.json.get('quatK').split(",")
                splitI = request.json.get('quatI').split(",")
                splitJ = request.json.get('quatJ').split(",")
                splitR = request.json.get('quatReal').split(",")
		entries.update_one({'sensorID':'sensor2'},
		{"$set": {'sensorID':request.json.get('sensorID'),
		'quatI':request.json.get('quatI'),
		'quatJ':request.json.get('quatJ'),
		'quatK':request.json.get('quatK'),
		'quatReal':request.json.get('quatReal'),
		'timestamp':str(datetime.datetime.now().time())}},
		upsert=True)
		for i in range(len(splitK)):
                    incTime = newTime + timedelta(microseconds=50000)
                    writeToCSV('sensor2',splitI[i],splitJ[i],splitK[i],splitR[i],str(incTime.time()))
                    newTime = datetime.datetime(2019, 4, 11, incTime.hour, incTime.minute, incTime.second, incTime.microsecond)
		return 'Data updated', 200
	elif request.method == 'GET':
		entry = entries.find_one({'sensorID':'sensor2'})
		print(entry)
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