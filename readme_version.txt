Linux: Ubuntu 16.04
Spark: without2 hadoop 2.4.0
Scala: 2.11.12
kafka: 0.8.2.2
Java: 1.8.0
spark-streaming-kafka: 0-8_2.11-2.4.0
hadoop:2.7.1
Python: 3.5
Flask: 0.12.1
Flask-SocketIO: 2.8.6
kafka-python： 1.3.3

#set up spark
cd /usr/local/spark
./bin/spark-shell   --master local[2]

# check topic:
bin/kafka-topics.sh --list --zookeeper localhost:2181

# Set up pycharm:
cd /usr/local/pycharm
./bin/pycharm.sh 

# Set up Kafka:
cd /usr/local/kafka
bin/zookeeper-server-start.sh config/zookeeper.properties 

cd /usr/local/kafka
bin/kafka-server-start.sh config/server.properties

cd /home/hadoop/PycharmProjects/streaming/scripts
python3 producer.py

cd /home/hadoop/PycharmProjects/streaming/scripts
python3 consumer.py

# set up Hadoop
cd /usr/local/hadoop  
./sbin/start-dfs.sh
./sbin/stop-dfs.sh

#startup

cd /usr/local/spark/mycode/kafka
sh startup.sh

## scala
cd /usr/local/spark/mycode/kafka
vim startup.sh
