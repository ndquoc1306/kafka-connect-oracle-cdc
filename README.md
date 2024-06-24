# Demonstration Oracle CDC Source Connector with Kafka Connect

## Clone this repo
```
https://github.com/ndquoc1306/kafka-connect-oracle-cdc.git
cd kafka-connect-oracle-cdc
```

## Get Oracle CDC Source Connector
Be sure to review license at https://www.confluent.io/hub/confluentinc/kafka-connect-oracle-cdc and download the zip file.

Unzip to `confluentinc-kafka-connect-oracle-cdc` (and remove any trailing version numbers)

```
unzip ~/Downloads/confluentinc-kafka-connect-oracle-cdc-1.0.3.zip
mv confluentinc-kafka-connect-oracle-cdc-1.0.3 confluentinc-kafka-connect-oracle-cdc
```


## Get Oracle Docker
From [Stackoverflow](https://stackoverflow.com/questions/47887403/pull-access-denied-for-container-registry-oracle-com-database-enterprise) ...


- log into https://hub.docker.com/
- search "oracle database"
- click on "Oracle Database Enterprise Edition"
- click on "Proceed to Checkout"
- fill in your contact info on the left, check two boxes under "Developer Tier" on the right, click on "Get Content"


```
docker login --username YourDockerUserName --password-stdin
<<Enter your password>>

docker pull ndquoc1306/oracledb:19c
```

# Docker Startup

- Install docker/docker-compose
- Set your Docker maximum memory to something really big, such as 10GB. (preferences -> advanced -> memory)
- Startup the platform (Oracle, Kafka, Kafka Connect, Schema registry)
```
docker-compose up -d
```


## Setup Oracle Docker
Once the Oracle database is running, we need to turn on ARCHIVELOG mode, create some users, and establish permissions

First, ensure the database looks like it's running (`docker-compose logs -f oracle`) and then run the following (for the curious, the SQL script is [here](scripts/oracle_setup_docker.sql) )

```
docker-compose exec oracle /scripts/go_sqlplus.sh /scripts/oracle_setup_docker
```

## Sample Data
This SQL script also creates tables



## Connector Configuration 

Check the OracleCdcSourceConnector source plug-in is available
```
curl -s -X GET -H 'Content-Type: application/json' http://localhost:8083/connector-plugins
```

And look for an occurrence of `"class": "io.confluent.connect.oracle.cdc.OracleCdcSourceConnector"`



Establish the `jsonCDC` connector
```
curl -s -X POST -H 'Content-Type: application/json' --data @/usr/share/java/confluentinc-kafka-connect-oracle-cdc/jsonCDC.json http://localhost:8083/connectors```

Check the status of the connector. You may need to wait a while for the status to show up
```
curl -s -X GET -H 'Content-Type: application/json' http://localhost:8083/connectors/jsonCDC/status
```



## Check topic
If you have Kafka tools installed locally, you can look at the de-serialised AVRO like this
```
exec kafka => kafka-console-consumer --bootstrap-server localhost:9092 --topic json --from-beginning
```


# Schema
Let's see what schemas we have registered now
```console
curl -s -X GET http://localhost:8081/subjects/ORCLCDB.C__BLOGWEBSITE.BLOG-value/versions/1
```

Amongst other things, you'll see version 1 of the schema has been registered like this
```
 ....
  ```
```



## Connector Delete Configuration 

If something goes wrong, you can delete the connector like this
```
curl -X DELETE localhost:8083/connectors/SimpleOracleCDC
```


# Tear down
To tear down the containers
```
docker-compose down
```# kafka-cdc-oracle
