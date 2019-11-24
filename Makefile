.PHONY: help
help:  ## Print this help menu
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: setup
setup:  ## Set up the local development environment
	poetry install -E tox
	poetry run pre-commit install

.PHONY: tox
test:  ## Run the tests
	poetry run tox

.PHONY: publish
publish:  ## Build & publish the new version
	poetry build
	poetry publish
