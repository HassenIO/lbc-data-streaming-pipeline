#!/bin/python3
import os
import pyspark

from pyspark.sql import SparkSession
from pyspark.sql.functions import window, col, json_tuple, from_unixtime, to_utc_timestamp, to_timestamp, count

print(pyspark.__version__)


# Initialize Spark Session
spark = SparkSession.builder.appName("kafkaToSpark").getOrCreate()


def main():
    # Read from Kafka topic
    df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "kafka:9092") \
        .option("subscribe", "dbserver1.inventory.customers") \
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
        .where("op == 'c'") \
        .withWatermark("ts_s", "10 seconds") \
        .groupBy(window("ts_s", "10 seconds")).count()

    # w = inserts_df.groupBy(window("ts_s", "10 seconds")).agg(count("op").alias("count"))
    # w.select(
    #     w.window.end.cast("string").alias("end_time"),
    #     "count"
    # )
    
    # inserts_df.groupBy(window("ts_s", "30 seconds")).count()

    # Write to the stream
    query = inserts_df \
        .writeStream \
        .outputMode("append") \
        .format("console") \
        .start()
    
    # Start the query and wait for it to terminate
    query.awaitTermination()


if __name__ == "__main__":
    main()

# NOTA: Run the following in a console:
# clear && spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 app.py
