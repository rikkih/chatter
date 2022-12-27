.PHONY: clean
clean:
	@find . | grep -E "(__pycache__)" | xargs rm -rf

.PHONY: runserver
runserver:
	@docker compose up --build

.PHONY: shell
shell:
	@docker compose exec -it app sh

.PHONY: build
build:
	@docker compose build

.PHONY: format
format:
	@python -m black core/chatter/ core/core/
