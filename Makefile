.PHONY: python-test
python-test:
	cd ./backend && pytest .

.PHONY: server
server:
	docker compose up

.PHONY: build
build:
	docker compose up --build