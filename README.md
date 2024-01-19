# Little Big Challenge

## To start the application

I created a bunch of make commands in the Makefile to help run the application.

To start the application and boot all the necessary services, run:

```bash
make up
```

This will run the docker compose and start the necessary containers:

- Zookeeper (used to manage Kafka)
- Kafka
- Kafdrop ([optional] used to visualize Kafka topics)
- PostgreSQL
- Debezium (used to capture changes in the PostgreSQL database, and streamline them to Kafka)
- MongoDB (used to store the final data aggregated data)
- JupyterLab (The notebook that we are going to use to run the code) -> Used for testing purposes

When the containers are up and running, you can access the JupyterLab notebook at http://localhost:8888/lab?token=xxx

(Have a look at the logs to get the real token value)

## Setup the environment

Setup the Kafka by creating the topics and connecting Debezium, by running the following make command:

```bash
make stream 
```

This will keep the connection open and streamlines all the events from PostgreSQL to Kafka. Each mutation operation to PostgreSQL will be catched and showed here.

To connect to the PostgreSQL database, you can use the following make command:

```bash
make pg
```

This will open a psql connection to the PostgreSQL database.

## Example manipulating data

Within the psql console, we can create a new customer with the following command:

```sql
INSERT INTO customers(id, first_name, last_name, email) VALUES (1005, 'Hassen', 'Taidirt', 'hi@hassen.io');
```

If you have opened both the psql console and Debezium connector console (with `make register`), you will see the mutation event in the Debezium console:

```json
{"schema":{"type":"struct","fields":[{"type":"struct","fields":[{"type":"int32","optional":false,"default":0,"field":"id"},{"type":"string","optional":false,"field":"first_name"},{"type":"string","optional":false,"field":"last_name"},{"type":"string","optional":false,"field":"email"}],"optional":true,"name":"dbserver1.inventory.customers.Value","field":"before"},{"type":"struct","fields":[{"type":"int32","optional":false,"default":0,"field":"id"},{"type":"string","optional":false,"field":"first_name"},{"type":"string","optional":false,"field":"last_name"},{"type":"string","optional":false,"field":"email"}],"optional":true,"name":"dbserver1.inventory.customers.Value","field":"after"},{"type":"struct","fields":[{"type":"string","optional":false,"field":"version"},{"type":"string","optional":false,"field":"connector"},{"type":"string","optional":false,"field":"name"},{"type":"int64","optional":false,"field":"ts_ms"},{"type":"string","optional":true,"name":"io.debezium.data.Enum","version":1,"parameters":{"allowed":"true,last,false,incremental"},"default":"false","field":"snapshot"},{"type":"string","optional":false,"field":"db"},{"type":"string","optional":true,"field":"sequence"},{"type":"string","optional":false,"field":"schema"},{"type":"string","optional":false,"field":"table"},{"type":"int64","optional":true,"field":"txId"},{"type":"int64","optional":true,"field":"lsn"},{"type":"int64","optional":true,"field":"xmin"}],"optional":false,"name":"io.debezium.connector.postgresql.Source","field":"source"},{"type":"string","optional":false,"field":"op"},{"type":"int64","optional":true,"field":"ts_ms"},{"type":"struct","fields":[{"type":"string","optional":false,"field":"id"},{"type":"int64","optional":false,"field":"total_order"},{"type":"int64","optional":false,"field":"data_collection_order"}],"optional":true,"name":"event.block","version":1,"field":"transaction"}],"optional":false,"name":"dbserver1.inventory.customers.Envelope","version":1},"payload":{"before":null,"after":{"id":1005,"first_name":"Hassen","last_name":"Taidirt","email":"hi@hassen.io"},"source":{"version":"2.1.4.Final","connector":"postgresql","name":"dbserver1","ts_ms":1705611172576,"snapshot":"false","db":"postgres","sequence":"[null,\"34487408\"]","schema":"inventory","table":"customers","txId":767,"lsn":34487408,"xmin":null},"op":"c","ts_ms":1705611172913,"transaction":null}}
```

The important part if the `payload` which parsed looks like this:

```json
"payload": {
     "before": null,
     "after":
     {
         "id": 1005,
         "first_name": "Hassen",
         "last_name": "Taidirt",
         "email": "hi@hassen.io"
     },
     "source":
     {
         "version": "2.1.4.Final",
         "connector": "postgresql",
         "name": "dbserver1",
         "ts_ms": 1705611172576,
         "snapshot": "false",
         "db": "postgres",
         "sequence": "[null,\"34487408\"]",
         "schema": "inventory",
         "table": "customers",
         "txId": 767,
         "lsn": 34487408,
         "xmin": null
     },
     "op": "c",
     "ts_ms": 1705611172913,
     "transaction": null
 }
```

As stated, this is a **CREATION** operation because we get a `"op": "c"` payload value and no before value (`"before": null`).

Back to the psql console, updating the previous record with the following update command:

```sql
UPDATE customers SET email='htaidirt@gmail.com' WHERE id=1005;
```

Will produce the following data capture:

```json
{"schema":{"type":"struct","fields":[{"type":"struct","fields":[{"type":"int32","optional":false,"default":0,"field":"id"},{"type":"string","optional":false,"field":"first_name"},{"type":"string","optional":false,"field":"last_name"},{"type":"string","optional":false,"field":"email"}],"optional":true,"name":"dbserver1.inventory.customers.Value","field":"before"},{"type":"struct","fields":[{"type":"int32","optional":false,"default":0,"field":"id"},{"type":"string","optional":false,"field":"first_name"},{"type":"string","optional":false,"field":"last_name"},{"type":"string","optional":false,"field":"email"}],"optional":true,"name":"dbserver1.inventory.customers.Value","field":"after"},{"type":"struct","fields":[{"type":"string","optional":false,"field":"version"},{"type":"string","optional":false,"field":"connector"},{"type":"string","optional":false,"field":"name"},{"type":"int64","optional":false,"field":"ts_ms"},{"type":"string","optional":true,"name":"io.debezium.data.Enum","version":1,"parameters":{"allowed":"true,last,false,incremental"},"default":"false","field":"snapshot"},{"type":"string","optional":false,"field":"db"},{"type":"string","optional":true,"field":"sequence"},{"type":"string","optional":false,"field":"schema"},{"type":"string","optional":false,"field":"table"},{"type":"int64","optional":true,"field":"txId"},{"type":"int64","optional":true,"field":"lsn"},{"type":"int64","optional":true,"field":"xmin"}],"optional":false,"name":"io.debezium.connector.postgresql.Source","field":"source"},{"type":"string","optional":false,"field":"op"},{"type":"int64","optional":true,"field":"ts_ms"},{"type":"struct","fields":[{"type":"string","optional":false,"field":"id"},{"type":"int64","optional":false,"field":"total_order"},{"type":"int64","optional":false,"field":"data_collection_order"}],"optional":true,"name":"event.block","version":1,"field":"transaction"}],"optional":false,"name":"dbserver1.inventory.customers.Envelope","version":1},"payload":{"before":{"id":1005,"first_name":"Hassen","last_name":"Taidirt","email":"hi@hassen.io"},"after":{"id":1005,"first_name":"Hassen","last_name":"Taidirt","email":"htaidirt@gmail.com"},"source":{"version":"2.1.4.Final","connector":"postgresql","name":"dbserver1","ts_ms":1705611235819,"snapshot":"false","db":"postgres","sequence":"[\"34488384\",\"34488440\"]","schema":"inventory","table":"customers","txId":768,"lsn":34488440,"xmin":null},"op":"u","ts_ms":1705611236197,"transaction":null}}
```

which the parsed payload looks like this:

```json
"payload": {
     "before":
     {
         "id": 1005,
         "first_name": "Hassen",
         "last_name": "Taidirt",
         "email": "hi@hassen.io"
     },
     "after":
     {
         "id": 1005,
         "first_name": "Hassen",
         "last_name": "Taidirt",
         "email": "htaidirt@gmail.com"
     },
     "source":
     {
         "version": "2.1.4.Final",
         "connector": "postgresql",
         "name": "dbserver1",
         "ts_ms": 1705611235819,
         "snapshot": "false",
         "db": "postgres",
         "sequence": "[\"34488384\",\"34488440\"]",
         "schema": "inventory",
         "table": "customers",
         "txId": 768,
         "lsn": 34488440,
         "xmin": null
     },
     "op": "u",
     "ts_ms": 1705611236197,
     "transaction": null
 }
```

with an update operation (`"op": "u"`) and a before value that is the previous value of the record.

In our PySpark, we need to access the `"op"` value of the payload, then only filter for the creation events (value is `c`).
