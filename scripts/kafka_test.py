from kafka import KafkaProducer
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from pyspark import SparkConf, SparkContext
import json
import sys

def KafkaWordCount(zkQuorum, group, topics, numThreads):
    spark_conf = SparkConf().setAppName("KafkaWordCount")
    sc = SparkContext(conf=spark_conf)
    ssc = StreamingContext(sc, 1)
    ssc.checkpoint('file:///usr/local/spark/mycode/kafka/checkpoint')
    # ssc.checkpoint(".")

    topicAry = topics.split(",")
    topicMap = {}
    for topic in topicAry:
        topicMap[topic] = numThreads
    lines = KafkaUtils.createStream(ssc, zkQuorum, group, topicMap).map(lambda x: x[1])
    words = lines.flatMap(lambda x: x.split(" "))
    wordcount = words.map(lambda x: (x, 1)).reduceByKeyAndWindow((lambda x, y: x + y), (lambda x, y: x - y), 1, 1, 1)
    wordcount.foreachRDD(lambda x: sendmsg(x))
    ssc.start()
    ssc.awaitTermination()

def Get_dic(rdd_list):
    res = []
    for elm in rdd_list:
        tmp = {elm[0]: elm[1]}
        res.append(tmp)
    return json.dumps(res)


def sendmsg(rdd):
    if rdd.count != 0:
        msg = Get_dic(rdd.collect())
        producer = KafkaProducer(bootstrap_servers='localhost:9092')
        producer.send("result", msg.encode('utf8'))
        producer.flush()


if __name__ == '__main__':
    # 输入的四个参数分别代表着
    # 1.zkQuorum为zookeeper地址
    # 2.group为消费者所在的组
    # 3.topics该消费者所消费的topics
    # 4.numThreads开启消费topic线程的个数
    if (len(sys.argv) < 5):
        print("Usage: KafkaWordCount <zkQuorum> <group> <topics> <numThreads>")
        exit(1)
    zkQuorum = sys.argv[1]
    group = sys.argv[2]
    topics = sys.argv[3]
    numThreads = int(sys.argv[4])
    print(group, topics)
    KafkaWordCount(zkQuorum, group, topics, numThreads)