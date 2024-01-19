build:
	docker build -t little-big-code-challenge-app .
.PHONY: build

up: # Start the containers using Docker compose
	docker compose up
.PHONY: up

rm: # Cleanup the containers
	docker compose rm -svf
.PHONY: rm

register: # Register the PG-Kafka connector
	curl -i -X POST \
		-H "Accept:application/json" \
		-H  "Content-Type:application/json" \
		http://localhost:8083/connectors/ \
		-d @register-postgres.json
.PHONY: register

stream: # Stream the data from the Kafka topic
	docker compose exec kafka /kafka/bin/kafka-console-consumer.sh \
		--bootstrap-server kafka:9092 \
		--from-beginning \
		--property print.key=true \
		--topic dbserver1.inventory.customers
.PHONY: stream

pg: # Connect to the Postgres database (psql)
	docker compose exec postgres env PGOPTIONS="--search_path=inventory" bash -c "psql -U $(POSTGRES_USER) postgres"
.PHONY: pg

sh: # Connect into the app with sh
	docker compose exec app sh
.PHONY: sh
