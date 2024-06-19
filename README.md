# Rating service

![GitHub release (latest by date)](https://img.shields.io/github/v/release/zuidui/rating-service)
![Docker Hub Image Version (latest by date)](https://img.shields.io/docker/v/zuidui/rating-service?label=docker%20hub)
![GitHub](https://img.shields.io/github/license/zuidui/rating-service)

## Description

This project is a simple service that provides information scores created to teams in the application, computes the average score of the team, and provides a rating based on the average score. Also publish the rating to a RabbitMQ queue.

## Prerequisites

Ensure you have the following installed on your system:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Project Structure

- `.github/`: Contains GitHub Actions workflows.
- `.vscode/`: Contains Visual Studio Code configurations for debugging.
- `.devcontainer/`: Contains configurations for the development container.
- `app/`
  - `wait-for-it.sh`: Helper script to wait for services to be ready.
  - `docker-compose.yml`: Defines the services, their configurations, and networking.
  - `Dockerfile`: Defines the Docker image for the API Gateway service.
  - `requirements.txt`: Lists the Python dependencies for the project.
  - `src/`: Contains the source code for the application.
    - `main.py`: Entry point for the FastAPI application.
    - `data/`: Database connection and session management.
    - `events/`: Event handling modules.
    - `exceptions/`: Custom exception classes.
    - `models/`: Database models.
    - `resolver/`: GraphQL resolvers.
    - `routes/`: FastAPI route definitions.
    - `service/`: Service layer for business logic.
    - `utils/`: Utility functions and configurations.
  - `tests/`: Contains the test files.
    - `acceptance/`: Acceptance tests.
    - `integration/`: Integration tests.
    - `unit/`: Unit tests.
- `chart/`
  - Helm charts for Kubernetes deployment.
- `CRD/`
  - Custom Resource Definitions for Kubernetes.
- `scripts/`: Contains helper scripts.
- `.env`: Environment variables used by Docker Compose and the application.
- `Makefile`: Provides a set of commands to automate common tasks.
- `LICENSE`: License file for the project.
- `README.md`: This file.

## Project Commands

The project uses [Makefiles](https://www.gnu.org/software/make/manual/html_node/Introduction.html) to run the most common tasks:

- `help`: Shows this help.
- `todo`: Shows the TODOs in the code.
- `show-env`: Shows the environment variables.
- `set-up`: Prepares the environment for development.
- `clean`: Cleans the app.
- `build`: Builds the app.
- `run`: Runs the app.
- `test`: Run all the tests.
- `test-unit`: Run the unit tests.
- `test-integration`: Run the integration tests.
- `test-acceptance`: Run the acceptance tests.
- `pre-commit`: Runs the pre-commit checks.
- `reformat`: Formats the code.
- `check-typing`: Runs a static analyzer over the code to find issues.
- `check-style`: Checks the code style.
- `publish-image-pre`: Publishes the image to the pre-production registry.
- `publish-image-pro`: Publishes the image to the production registry.

## Services

**API Gateway**: `http://${IMAGE_NAME}:${APP_PORT}`

**Sanity Check**: `http://${IMAGE_NAME}:${APP_PORT}/health`

**Schema Definition**: `http://${IMAGE_NAME}:${APP_PORT}/schema`

**API Documentation**: `http://${IMAGE_NAME}:${APP_PORT}/{DOC_URL}`

**GraphQL Playground**: `http://${IMAGE_NAME}:${APP_PORT}/api/{API_PREFIX}/graphql`

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a Pull Request.

## License

This project is licensed under the Apache 2.0 License. See the LICENSE file for details.

## Contact

For any inquiries or issues, please open an issue on the [GitHub repository](https://github.com/zuidui/rating-service) or contact any of the maintainers.
