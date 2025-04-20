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

# 例）make test tag=all, make test
.PHONY: test
test:
	@cd backend && if [ "$(tag)" = "all" ]; then \
		pipenv run pytest .; \
	else \
		pipenv run pytest -k "not test_quiz_creator.py" .; \
	fi