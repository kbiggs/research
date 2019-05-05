import json
import time
import logging
import http.client
import requests
import sys
import datetime

#SERVER = 'http://127.0.0.1:5000'
SERVER = 'http://192.168.137.227:80'

http.client.HTTPConnection.debuglevel = 1

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

session = requests.Session()

while (True):
	r = session.get(SERVER)
	time.sleep(2)

	sensor1_payload = {
		'sensorID':'sensor1',
		'quatI':'3.14,3.14,3.14,3.14,3.14,3.14,3.14,3.14,3.14,3.14',
		'quatJ':'3.14,3.14,3.14,3.14,3.14,3.14,3.14,3.14,3.14,3.14',
		'quatK':'3.14,3.14,3.14,3.14,3.14,3.14,3.14,3.14,3.14,3.14',
		'quatReal':'3.14,3.14,3.14,3.14,3.14,3.14,3.14,3.14,3.14,3.14',
		'timestamp':'15:47:54.584114'
	}

	#update server with the above payload
	r = session.post(SERVER + "/sensor1", json=sensor1_payload)
	time.sleep(2)

	#query server-should see the above payload printed back out
	r = session.get(SERVER + "/sensor1")
	data = json.loads(r.text)
	print(data)
	time.sleep(2)


	sensor2_payload = {
		'sensorID':'sensor2',
		'quatI':'1',
		'quatJ':'2',
		'quatK':'3',
		'quatReal':'6',
		'timestamp':'15:47:54.584114'
	}

	#update server with the above payload
	r = session.post(SERVER + "/sensor2", json=sensor2_payload)
	time.sleep(2)

	#query server-should see the above payload printed back out
	r = session.get(SERVER + "/sensor2")
	data = json.loads(r.text)
	print(data)
	time.sleep(2)