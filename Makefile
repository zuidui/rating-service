.DEFAULT_GOAL := help

include app/.env

export REGISTRY_PRE=$(DOCKERHUB_USERNAME)/$(IMAGE_NAME)-dev
export REGISTRY_PRO=$(DOCKERHUB_USERNAME)/$(IMAGE_NAME)
export TAGS=$(shell curl -s "https://hub.docker.com/v2/repositories/${REGISTRY_PRE}/tags/" | jq -r '.results[].name'| grep -E 'rc[0-9]{2}' | tr '\n' ' ')
export LATEST_TAG := $(if $(TAGS),$(lastword $(sort $(TAGS))),00)
export LATEST_VERSION := $(shell echo "$(LATEST_TAG)" | sed -E 's/([0-9]+\.[0-9]+\.[0-9]+)-rc[0-9]{2}+/\1/')
export LATEST_RC := $(if $(filter-out 00,$(LATEST_TAG)),$(shell echo "$(LATEST_TAG)" | sed -E 's/^.*-rc([0-9]{2})$$/\1/'),00)
ifeq ($(IMAGE_VERSION),$(LATEST_VERSION))
NEXT_RC := $(shell sh -c 'if [ "$(LATEST_RC)" -eq "08" ]; then printf "%02d" 9; elif [ "$(LATEST_RC)" -eq "09" ]; then printf "%02d" 10; else printf "%02d" $$(($(LATEST_RC) + 1)); fi')
else
NEXT_RC := 00
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
	@echo "REGISTRY_PRE: $(REGISTRY_PRE)"
	@echo "REGISTRY_PRO: $(REGISTRY_PRO)"
	@echo "TAGS: $(TAGS)"
	@echo "LATEST_TAG: $(LATEST_TAG)"
	@echo "IMAGE_VERSION: $(IMAGE_VERSION)"
	@echo "LATEST_VERSION: $(LATEST_VERSION)"
	@echo "LATEST_RC: $(LATEST_RC)"
	@echo "NEXT_RC: $(NEXT_RC)"

.PHONY: set-up
set-up: ## Prepare the environment for debugging.
	@echo "Preparing $(IMAGE_NAME) for debugging."
	@./scripts/create-requirements.sh

.PHONY: start-db 
start-db:  ## Start the database.
	@echo "Starting the database."
	@docker-compose -f $(SRC_PATH)/docker-compose.yml up -d db pgadmin
	@./scripts/wait-for-it.sh db:$(DB_PORT) --timeout=5 -- echo "Database is up and running"

.PHONY: clean
clean:  ## Clean the app.
	@echo "Cleaning $(IMAGE_NAME) docker image."
	docker-compose -f ./app/docker-compose.yml down --rmi all --volumes

.PHONY: build
build:  ## Build the app.
	@echo "Building $(IMAGE_NAME) docker image as $(IMAGE_NAME):$(IMAGE_VERSION)."
	docker build -t $(REGISTRY_PRE):$(IMAGE_VERSION) ./app

.PHONY: run
run:  pre-commit ## Start the app in development mode.
	@echo "Starting $(IMAGE_NAME) in development mode."
	docker-compose -f ./app/docker-compose.yml up --build $(IMAGE_NAME)

# TODO: Implement tests
.PHONY: test
test: ## Run the unit, integration and acceptance tests.
	@echo "Running the unit, integration and acceptance tests."
	docker-compose -f ./app/docker-compose.yml run --rm $(IMAGE_NAME) pytest -n 4 /workspace/app/tests -ra

.PHONY: pre-commit
pre-commit:  ## Run the pre-commit checks.
	@echo "Running the pre-commit checks."
	$(MAKE) reformat
	$(MAKE) check-typing
	$(MAKE) check-style

.PHONY: check-typing
check-typing:  ## Check the typing.
	@echo "Checking the typing."
	docker-compose -f ./app/docker-compose.yml run --rm $(IMAGE_NAME) mypy .

.PHONY: check-style
check-style:  ## Check the styling.
	@echo "Checking the styling."
	docker-compose -f ./app/docker-compose.yml run --rm $(IMAGE_NAME) ruff check .
	
.PHONY: reformat
reformat:  ## Reformat the code.
	@echo "Reformatting the code."
	docker-compose -f ./app/docker-compose.yml run --rm $(IMAGE_NAME) ruff format .

.PHONY: publish-image-pre
publish-image-pre: build ## Push the release candidate to the registry.
	@echo "Publishing the image as release candidate -  $(REGISTRY_PRE):$(IMAGE_VERSION)-rc$(NEXT_RC)"
	@docker tag $(REGISTRY_PRE):$(IMAGE_VERSION) $(REGISTRY_PRE):$(IMAGE_VERSION)-rc$(NEXT_RC)
	@docker tag $(REGISTRY_PRE):$(IMAGE_VERSION) $(REGISTRY_PRE):latest
	@docker push $(REGISTRY_PRE):$(IMAGE_VERSION)-rc$(NEXT_RC)
	@docker push $(REGISTRY_PRE):latest

## TODO: Check if the latest version is the same as the image version error when creating release in GitHub
.PHONY: publish-image-pro
publish-image-pro:  ## Publish the latest release to the registry.
	@echo "Publishing the latest image in the registry - $(REGISTRY_PRO):$(LATEST_VERSION)"
	@docker pull $(REGISTRY_PRE):$(LATEST_TAG)
	@docker tag $(REGISTRY_PRE):$(LATEST_TAG) $(REGISTRY_PRO):latest
	@docker tag $(REGISTRY_PRE):$(LATEST_TAG) $(REGISTRY_PRO):$(LATEST_VERSION)
	@docker push $(REGISTRY_PRO):$(LATEST_VERSION)
	@docker push $(REGISTRY_PRO):latest
##@if [ "$(LATEST_VERSION)" == "$(IMAGE_VERSION)" ]; then git tag -d $(LATEST_VERSION); fi
##@git tag -a $(LATEST_VERSION) -m "Release $(LATEST_VERSION)"	
##@if [ "$(LATEST_VERSION)" == "$(IMAGE_VERSION)" ]; then git release delete $(LATEST_VERSION); fi
##@gh release create $(LATEST_VERSION) -t $(LATEST_VERSION) -n $(LATEST_VERSION)
##@git push origin $(LATEST_VERSION)	