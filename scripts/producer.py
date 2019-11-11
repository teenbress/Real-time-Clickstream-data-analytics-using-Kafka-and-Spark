import csv
import time
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='localhost:9092')
csvfile = open("user_log.csv", "r")
reader = csv.reader(csvfile)

for line in reader:
    gender = line[9]
    if gender == 'gender':
        continue
    time.sleep(0.1)
    producer.send('sex', line[9].encode('utf8'))