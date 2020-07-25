from confluent_kafka import Consumer, KafkaError, Producer
import time, sys, json, socket, os
from datetime import datetime

p = Producer({'bootstrap.servers': "localhost:9092"})

def run_actionNotify(value):
	if value>=10 and value<=59:
		message= "Your {} at {} had a LOW TEMPERATURE of {} in {}".format(sys.argv[3], str(datetime.now()), str(value), sys.argv[8])
	elif value>=60 and value<=100:
		message= "Your {} at {} had a NORMAL TEMPERATURE of {} in {}".format(sys.argv[3], str(datetime.now()), str(value), sys.argv[8])
	elif value>=101 and value<+120:
		message= "Your {} at {} had a HIGH TEMPERATURE of {} in {}".format(sys.argv[3], str(datetime.now()), str(value), sys.argv[8])
	else:
		return

	notify_data= {'notify_type': "",
				  'app_name' : sys.argv[2],
				  'service' : sys.argv[3],
				  'username' : sys.argv[4],
				  'phone_number' : sys.argv[5],
				  'email' : sys.argv[6],
				  'firstname' : sys.argv[7],
				  'message' : message
	}

	notify_data= json.dumps(notify_data)
	p.produce('notify', notify_data.encode('utf-8'))
	p.poll(0)


c = Consumer({'bootstrap.servers': "localhost:9092", 'group.id': sys.argv[1], 'auto.offset.reset': 'latest'})
c.subscribe(["temp_ac"])
while True:
	msg = c.poll(1.0)

	if msg is None or msg.error():
		continue

	# print ("####", sys.argv[2], sys.argv[3],sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7])
	value= int((msg.value()).decode('utf-8'))
	# print("****value= ", value, "******")
	run_actionNotify(value)