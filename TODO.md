To start the example of Debezium with Postgres and Kafka, simply run the docker compose file:

```
export DEBEZIUM_VERSION=2.1
docker compose up
```

When everything is up, register the PG-Kafka connector with the following CURL command:

```
curl -i -X POST -H "Accept:application/json" -H  "Content-Type:application/json" http://localhost:8083/connectors/ -d @register-postgres.json
```

To start the Kafka consumer and watch the actions on the Postgres database:

```
docker compose exec kafka /kafka/bin/kafka-console-consumer.sh \
    --bootstrap-server kafka:9092 \
    --from-beginning \
    --property print.key=true \
    --topic dbserver1.inventory.customers
```

Open the Postgres console to add commands to watch in Kafka:

```
docker compose exec postgres env PGOPTIONS="--search_path=inventory" bash -c 'psql -U $POSTGRES_USER postgres'
```

If you want to access the shell of the Postgres container (to get access to PG configs for example or read the connectors):

```
docker exec -it little-big-code-challenge-postgres-1 sh
```
