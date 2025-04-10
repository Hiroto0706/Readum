.PHONY: python-test
python-test:
	cd ./backend && pytest .

.PHONY: server
server:
	docker compose up

.PHONY: build
build:
	docker compose up --build

.PHONY: server-as-prd
server-as-prd:
	docker compose -f docker-compose.prd.yml up --build