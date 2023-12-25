#!/bin/bash

# Wait for Kafka to be ready for up to MAX_WAIT seconds
# MAX_WAIT=1200
# COUNT=0
# while ! nc -z kafka 9092; do
#     sleep 1
#     COUNT=$((COUNT+1))
#     echo "Waiting for Kafka to be ready: $COUNT seconds elapsed (max=$MAX_WAIT)..."
#     if [ $COUNT -gt $MAX_WAIT ]; then
#         echo "Kafka did not start within $MAX_WAIT seconds. Exiting."
#         exit 1
#     fi
# done

START_TIMEOUT=600
count=0
step=10

echo "waiting for kafka to be ready"
while netstat -lnt | awk '$4 ~ /:'"9092"'$/ {exit 1}'; do
    sleep $step;
    count=$((count + step))
    echo "waited Kafka to start for $count seconds so far..."
    if [ $count -gt $START_TIMEOUT ]; then
        echo "Not able to auto-create topic (waited for $START_TIMEOUT sec)"
        exit 1
    fi
done

# Create the desired Kafka topics
echo "Kafka is ready. Creating Kafka topics..."
kafka-topics --create \
    --topic creations-topic \
    --partitions 1 \
    --replication-factor 1 \
    --if-not-exists \
    --zookeeper zookeeper:2181 \
    --bootstrap-server kafka:9092
# NOTA: Add here more topics if needed

echo "Kafka's topics created successfully."

# Keep the script running (so we keep the container running)
# tail -f /dev/null
wait
