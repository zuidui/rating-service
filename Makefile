.DEFAULT_GOAL := help

include ./app/.env

export TAGS=$(shell curl -s "https://hub.docker.com/v2/repositories/${REGISTRY}/tags/" | jq -r '.results[].name'| grep -E 'rc[0-9]{2}' | tr '\n' ' ')
export LATEST_TAG := $(if $(TAGS),$(lastword $(sort $(TAGS))),00)
export LATEST_VERSION := $(shell echo "$(LATEST_TAG)" | sed -E 's/([0-9]+\.[0-9]+\.[0-9]+)-rc[0-9]{2}+/\1/')
export LATEST_RC := $(if $(filter-out 00,$(LATEST_TAG)),$(shell echo "$(LATEST_TAG)" | sed -E 's/^.*-rc([0-9]{2})$$/\1/'),00)
ifneq ($(IMAGE_VERSION),$(LATEST_VERSION))
	NEXT_RC := 00
else
	NEXT_RC := $(if $(filter-out 00,$(LATEST_TAG)),$(shell printf "%02d" $$(($(LATEST_RC) + 1))),00)
endif
export NEXT_RC

.PHONY: help
help:  ## Show this help.
	@grep -E '^\S+:.*?## .*$$' $(firstword $(MAKEFILE_LIST)) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "%-30s %s\n", $$1, $$2}'

.PHONY: todo
todo:  ## Show the TODOs in the code.
	@{ grep -n -w TODO Makefile | uniq || echo "No pending tasks"; } | sed '/grep/d'

.PHONY: show-env
show-env:  ## Show the environment variables.
	@echo "Showing the environment variables."
	@echo "REGISTRY: $(REGISTRY)"
	@echo "TAGS: $(TAGS)"
	@echo "LATEST_TAG: $(LATEST_TAG)"
	@echo "IMAGE_VERSION: $(IMAGE_VERSION)"
	@echo "LATEST_VERSION: $(LATEST_VERSION)"
	@echo "LATEST_RC: $(LATEST_RC)"
	@echo "NEXT_RC: $(NEXT_RC)"

.PHONY: build
build:  ## Build the app.
	@echo "Building $(APP_NAME) docker image as $(IMAGE_NAME):$(IMAGE_VERSION)."
	docker build -t $(REGISTRY):$(IMAGE_VERSION) $(CONTAINER_NAME)

.PHONY: clean
clean:  ## Clean the app.
	@echo "Cleaning $(CONTAINER_NAME) docker image."
	docker-compose -f $(CONTAINER_NAME)/docker-compose.yml down --rmi all --volumes --remove-orphans

.PHONY: run
run:  ## Start the app in development mode.
	@echo "Starting $(APP_NAME) in development mode."
	docker-compose -f $(CONTAINER_NAME)/docker-compose.yml up --build $(CONTAINER_NAME)

.PHONY: poetry-init
poetry-init:  ## Initialize the poetry project and install the dependencies.
	@echo "Initializing the poetry project and installing the dependencies."
	cd app && poetry init -n --name $(APP_NAME) --version $(APP_VERSION) --author $(AUTHOR) --description $(DESCRIPTION) --license $(LICENSE) --python $(PYTHON_VERSION) && poetry add $(DEPENDENCIES)

.PHONY: install
install:  ## Install a new package in the app. ex: make install pkg=package_name
	@echo "Installing a package $(pkg) in the $(CONTAINER_NAME) docker image."
	docker-compose -f $(CONTAINER_NAME)/docker-compose.yml run --rm $(CONTAINER_NAME) poetry add $(pkg)@latest
	$(MAKE) build

.PHONY: uninstall
uninstall:  ## Uninstall a package from the app. ex: make uninstall pkg=package_name
	@echo "Uninstalling a package $(pkg) from the $(CONTAINER_NAME) docker image."
	docker-compose -f $(CONTAINER_NAME)/docker-compose.yml run --rm $(CONTAINER_NAME) poetry remove $(pkg)
	$(MAKE) build

## TODO: Tag the image in git  - check with GithubActions
.PHONY: publish-image-rc
publish-image-rc: build ## Push the release candidate to the registry.
	@echo "Publishing the image as release candidate -  $(REGISTRY):$(IMAGE_VERSION)-rc$(NEXT_RC)"
	docker tag $(REGISTRY):$(IMAGE_VERSION) $(REGISTRY):$(IMAGE_VERSION)-rc$(NEXT_RC)
	docker push $(REGISTRY):$(IMAGE_VERSION)-rc$(NEXT_RC)

.PHONY: publish-image-latest
publish-image-latest:  build ## Publish the latest release to the registry.
	@echo "Publishing the latest image as latest- $(REGISTRY):$(LATEST_TAG) as latest"
	docker pull $(REGISTRY):$(LATEST_TAG)
	docker tag $(REGISTRY):$(LATEST_TAG) $(REGISTRY):latest
	docker push $(REGISTRY):latest

.PHONY: test
test:  ## Run the unit, integration and acceptance tests.
	@echo "Running the unit, integration and acceptance tests."
	$(MAKE) test-unit
	$(MAKE) test-integration
	$(MAKE) test-acceptance

.PHONY: pre-commit
pre-commit:  ## Run the pre-commit checks.
	@echo "Running the pre-commit checks."
	$(MAKE) reformat
	$(MAKE) check-typing
	$(MAKE) check-style

.PHONY: check-typing
check-typing:  ## Check the typing.
	@echo "Checking the typing."
	docker-compose -f $(CONTAINER_NAME)/docker-compose.yml run --rm $(CONTAINER_NAME) poetry run mypy .

.PHONY: check-style
check-style:  ## Check the styling.
	@echo "Checking the styling."
	docker-compose -f $(CONTAINER_NAME)/docker-compose.yml run --rm $(CONTAINER_NAME) poetry run ruff check .
	
.PHONY: reformat
reformat:  ## Reformat the code.
	@echo "Reformatting the code."
	docker-compose -f $(CONTAINER_NAME)/docker-compose.yml run --rm $(CONTAINER_NAME) poetry run ruff format .

.PHONY: test-unit
test-unit:  ## Run the unit tests.
	@echo "Running the unit tests."
	docker-compose -f $(CONTAINER_NAME)/docker-compose.yml run --rm $(CONTAINER_NAME) poetry run pytest -n 4 tests/unit -ra 

.PHONY: test-acceptance
test-acceptance:  ## Run the acceptance tests.
	@echo "Running the acceptance tests."
	docker-compose -f $(CONTAINER_NAME)/docker-compose.yml run --rm $(CONTAINER_NAME) poetry run pytest -n 4 tests/acceptance -ra
	
.PHONY: test-integration
test-integration:  ## Run the integration tests.
	@echo "Running the integration tests."
	docker-compose -f $(CONTAINER_NAME)/docker-compose.yml run --rm $(CONTAINER_NAME) poetry run pytest -n 4 tests/integration -ra