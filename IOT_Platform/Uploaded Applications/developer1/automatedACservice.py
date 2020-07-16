from confluent_kafka import Consumer, KafkaError, Producer
import time, sys, json, socket, os

p = Producer({'bootstrap.servers': "localhost:9092"})

def run_actionNotify(value):

	notify_data= {'notify_type': "email",
				  'app_name' : sys.argv[2],
				  'service' : sys.argv[3],
				  'username' : sys.argv[4],
				  'phone_number' : sys.argv[5],
				  'email' : sys.argv[6],
				  'firstname' : sys.argv[7],
				  'value' : value
	}

	notify_data= json.dumps(notify_data)
	p.produce('notify', notify_data.encode('utf-8'))
	p.poll(0)


c = Consumer({'bootstrap.servers': "localhost:9092", 'group.id': sys.argv[1], 'auto.offset.reset': 'latest'})
c.subscribe(["temp_ac"])
print ("************************************in service", os.getpid(), "*******************************************")
while True:
	msg = c.poll(1.0)

	if msg is None or msg.error():
		continue

	# print ("####", sys.argv[2], sys.argv[3],sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7])
	value= int((msg.value()).decode('utf-8'))
	# print("****value= ", value, "******")
	run_actionNotify(value)