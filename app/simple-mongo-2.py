#!/bin/python3
import os
import pyspark
import pymongo
from pymongo import MongoClient

from pyspark.sql import SparkSession
from pyspark.sql.functions import window, col, json_tuple, from_unixtime, to_utc_timestamp, to_timestamp, count

print(pyspark.__version__)


# Initialize Spark Session
spark = SparkSession.builder.appName("kafkaToSpark").getOrCreate()


def write_machine_df_mongo(target_df):
    cluster = MongoClient("mongodb://mongo:27017")
    db = cluster["local"]
    collection = db.creations

    post = { "time": target_df.ts_s }

    collection.insert_one(post)


def main():
    # Read from Kafka topic
    df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "kafka:9092") \
        .option("subscribe", "dbserver1.inventory.customers") \
        .option("spark.mongodb.write.connection.uri", "mongodb://mongo:27017/local.creations?convertJson=any") \
        .load()

    # Define the selector expression
    inserts_df = df \
        .selectExpr("CAST(key AS STRING) as key", "CAST(value AS STRING) as value", "topic") \
        .select("value") \
        .select(json_tuple(col("value"), "payload")) \
        .toDF("payload") \
        .select("payload") \
        .select(json_tuple(col("payload"), "op", "ts_ms")) \
        .toDF("op", "ts_ms") \
        .withColumn("ts_s", to_timestamp(col("ts_ms") / 1000)) \
        .where("op == 'c'")
        # \
        # .withWatermark("ts_s", "10 seconds") \
        # .groupBy(window("ts_s", "10 seconds")) \
        # .count()

    # Write to the stream
    # inserts_df.writeStream \
    #     .format("mongodb") \
    #     .option("checkpointLocation", "/tmp/pyspark/") \
    #     .option("forceDeleteTempCheckpointLocation", "true") \
    #     .start() \
    #     .awaitTermination()

    inserts_df.writeStream \
        .outputMode("append") \
        .foreach(write_machine_df_mongo) \
        .start() \
        .awaitTermination()


if __name__ == "__main__":
    main()

# NOTA: Run the following in a console:
# clear && spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,org.mongodb.spark:mongo-spark-connector_2.12:10.2.1 app.py
