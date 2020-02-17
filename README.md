# delta-architecture
A data pipeline that maintains an up to date replication of multiple databases
It is composed of Debezium and Delta Lake:
- Debezium: Debezium is an open source distributed platform for change data capture. Start it up, point it at your databases, and your apps can start responding to all of the inserts, updates, and deletes that other apps commit to your databases. Debezium is durable and fast, so your apps can respond quickly and never miss an event, even when things go wrong.
https://debezium.io
- Delta Lake: Delta Lake is an open-source storage layer that brings ACID transactions to Apache Spark™ and big data workloads.
https://delta.io

## Strategy
- Debezium reads database log, produces json messages that describe the changes made and streams them to Kafka
- Kafka streams the messages and stores in an S3 folder. We call it "Bronze" table as it stores raw messages
- Using Spark with Delta Lake we transform the messages to INSERT, UPDATE and DELETE operations, and run them on the replicated data table. We call it "Silver" table as it's a refined table that holds the latest state of all source databases
- Next we can perform further aggregations on the Silver table for analytics. We call it "Gold" table

## Components
- Debezium Stack - Kafka, Zookeepr and Kafka-Connect: Reads changes from the Databases and streams it to S3
- Delta Transformer: PySpark code that transforms Debezium messages to INSERT, UPDATE and DELETE operations
- fake_it: A simulator of an application database with live input

## Instructions
-
