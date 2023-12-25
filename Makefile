build:
	docker build -t little-big-code-challenge-app .
.PHONY: build

start:
	docker compose up
.PHONY: start

rm:
	docker compose rm -svf
.PHONY: rm
