import kafka
consumer = kafka.KafkaConsumer(group_id='SimpleOracleCDC-0-ORCLCDB-C##BLOGWEBSITE-BLOG',
                               bootstrap_servers=['localhost:9092'])
print("Topics available for connection:", consumer.topics())
