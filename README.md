WORK-IN-PROGRESS

# delta-architecture
Streaming data changes to a Data Lake with Debezium and Delta Lake pipeline
https://medium.com/@yinondn_94470/streaming-data-changes-to-a-data-lake-with-debezium-and-delta-lake-pipeline-786d6f2ddc32

This is an example end-to-end project that demonstrates the Debezium-Delta Lake combo pipeline
See medium post for more details

## High Level Strategy Overview
- Debezium reads database logs, produces json messages that describe the changes made and streams them to Kafka
- Kafka streams the messages and stores them in a S3 folder. We call it "Bronze" table as it stores raw messages
- Using Spark with Delta Lake we transform the messages to INSERT, UPDATE and DELETE operations, and run them on the target data table. We call it "Silver" table as it holds the latest state of all source databases
- Next we can perform further aggregations on the Silver table for analytics. We call it "Gold" table

## Components
- compose: Docker-Compose configuration that deploys Debezium stack (Kafka, Zookeepr and Kafka-Connect), reads changes from the source databases and streams them to S3
- voter-processing: PySpark code that transforms Debezium messages to INSERT, UPDATE and DELETE operations
- fake_it: For an end-to-end example, a simulator of an application's database with live input

## Instructions
### Start up docker compose
- export DEBEZIUM_VERSION=1.0
- cd compose
- docker-compose up -d
### Config Debezium connector
curl -i -X POST -H "Accept:application/json" -H  "Content-Type:application/json" http://localhost:8084/connectors/ -d @debezium/config.json
