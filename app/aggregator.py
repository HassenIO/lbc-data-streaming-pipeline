from pyspark.sql import SparkSession
from pyspark.sql.functions import window, col


# Initialize Spark Session
spark = SparkSession.builder.appName("kafkaToSpark").getOrCreate()


def main():
    # Read from Kafka topic
    print("Reading from Kafka topic...")
    df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "kafka:9092") \
        .option("subscribe", "test") \
        .load()

    # Select only "insert" operations and count them per 10-seconds window
    print("Counting insert operations per 10-seconds window...")
    inserts = df \
        .selectExpr("CAST(value AS STRING)") \
        .where("value.operation == 'c'") \
        .groupBy(window(col("timestamp"), "10 seconds")) \
        .count()

    # Write the aggregation result to MongoDB
    print("Writing aggregation result to MongoDB...")
    inserts.writeStream \
        .format("mongo") \
        .option("uri", "mongodb://mongodb:27017/local.creations") \
        .start() \
        .awaitTermination()


if __name__ == "__main__":
    print("Aggregator is running...")
    main()
    print("Aggregator has stopped...")
