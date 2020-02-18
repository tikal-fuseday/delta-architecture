# delta-architecture
A data pipeline that maintains an up to date replication of multiple databases

It is composed of Debezium and Delta Lake:
- Debezium is an open source distributed platform for change data capture. Start it up, point it at your databases, and your apps can start responding to all of the inserts, updates, and deletes that other apps commit to your databases. Debezium is durable and fast, so your apps can respond quickly and never miss an event, even when things go wrong.
https://debezium.io
- Delta Lake is an open-source storage layer that brings ACID transactions to Apache Spark™ and big data workloads.
https://delta.io

## Strategy
- Debezium reads database logs, produces json messages that describe the changes made and streams them to Kafka
- Kafka streams the messages and stores them in a S3 folder. We call it "Bronze" table as it stores raw messages
- Using Spark with Delta Lake we transform the messages to INSERT, UPDATE and DELETE operations, and run them on the target data table. We call it "Silver" table as it holds the latest state of all source databases
- Next we can perform further aggregations on the Silver table for analytics. We call it "Gold" table

## Components
- compose: Docker-Compose that deploys Debezium stack (Kafka, Zookeepr and Kafka-Connect), reads changes from the Databases and streams them to S3
- delta-processor: PySpark code that transforms Debezium messages to INSERT, UPDATE and DELETE operations
- fake_it: For an end-to-end example, a simulator of an application's database with live input

## Instructions
### Start up docker compose
- export DEBEZIUM_VERSION=1.0
- cd compose
- docker-compose up -d
### Config Debezium connector
curl -i -X POST -H "Accept:application/json" -H  "Content-Type:application/json" http://localhost:8084/connectors/ -d @debezium/config.json
