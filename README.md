# How to test Kafka manually

To test that Kafka is working properly, you can use Kafka command-line tools or create a simple producer and consumer in your preferred programming language. Here, I'll provide instructions for testing Kafka using command-line tools.

1. **Create a Topic**:

   Before you can produce and consume messages, you need to create a Kafka topic. You can use the Kafka command-line tool to do this. Open a terminal and run the following command to create a topic named "test-topic":

   ```bash
   docker exec -it kafka kafka-topics --create --topic test-topic --partitions 1 --replication-factor 1 --bootstrap-server localhost:9092
   ```

2. **Produce Messages**:

   To produce messages to the "test-topic" topic, you can use the Kafka console producer. Run the following command to produce a message:

   ```bash
   docker exec -it kafka kafka-console-producer --topic test-topic --broker-list localhost:9092
   ```

   After running this command, you can start typing messages, and each line you enter will be sent as a Kafka message.

3. **Consume Messages**:

   To consume messages from the "test-topic" topic, you can use the Kafka console consumer. Open a new terminal window and run the following command:

   ```bash
   docker exec -it kafka kafka-console-consumer --topic test-topic --from-beginning --bootstrap-server localhost:9092
   ```

   This command will display the messages that you produce in step 2. You should see the messages you entered in the producer terminal.

4. **Verify Kafka Functionality**:

   To further test Kafka's functionality, you can produce and consume more messages, experiment with different topics, and explore Kafka's features such as partitions and consumer groups.

By following these steps, you can confirm that Kafka is working properly in your Docker container. If you encounter any issues or want to explore more advanced Kafka features, you can refer to the official Kafka documentation for more detailed information and examples: [Apache Kafka Documentation](https://kafka.apache.org/documentation/).
