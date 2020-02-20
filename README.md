WORK-IN-PROGRESS

# delta-architecture
Streaming data changes to a Data Lake with Debezium and Delta Lake pipeline
https://medium.com/@yinondn_94470/streaming-data-changes-to-a-data-lake-with-debezium-and-delta-lake-pipeline-786d6f2ddc32

This is an example end-to-end project that demonstrates the Debezium-Delta Lake combo pipeline

See medium post for more details

## High Level Strategy Overview
- Debezium reads database logs, produces json messages that describe the changes and streams them to Kafka
- Kafka streams the messages and stores them in a S3 folder. We call it Bronze table as it stores raw messages
- Using Spark with Delta Lake we transform the messages to INSERT, UPDATE and DELETE operations, and run them on the target data lake table. This is the table that holds the latest state of all source databases. We call it Silver table
- Next we can perform further aggregations on the Silver table for analytics. We call it Gold table

## Components
- compose: Docker-Compose configuration that deploys containers with Debezium stack (Kafka, Zookeepr and Kafka-Connect), reads changes from the source databases and streams them to S3
- voter-processing: Notebook with PySpark code that transforms Debezium messages to INSERT, UPDATE and DELETE operations
- fake_it: For an end-to-end example, a simulator of a voters book application's database with live input

## Instructions
### Start up docker compose
- export DEBEZIUM_VERSION=1.0
- cd compose
- docker-compose up -d
### Config Debezium connector
curl -i -X POST -H "Accept:application/json" -H  "Content-Type:application/json" http://localhost:8084/connectors/ -d @debezium/config.json
### Run spark notebook
Import the notebook file in \voter-processing\voter-processing.html to a Databricks Community account and follow the instructions inside the notebook


https://community.cloud.databricks.com/

## TODO - To complete the end-to-end example flow
- Change the voter-processing from notebook to PySpark application
- Add the PySpark application to the Docker-Compose
- Change the configurations so that Kafka writes to local file system instead of S3
- Change the Spark application so that it read Kafka's output instead of generating it's own mock data

## What's Next?
Make it a configurable generic tool that can be assembled on top of any supported database