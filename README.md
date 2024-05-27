# Users microservice

## Description

Proof of concept for the Master's Thesis. Main objectives are:

- Create a simple web application with FastAPI
- Follow best practices to structure the application
- Demo to authenticate users, store data in a database and retrieve it
- Apply TDD to the development of the application. Unit tests and integration tests
- Use Redis to store the session data and cache
- Use Docker to deploy the application
- SQLModel to interact with the database
- Use GitHub Actions to automate the CI/CD pipeline

## Requirements

- You only need to have [Docker](https://www.docker.com/) installed.

## Folder structure

- There is a `tests` folder with the tests files.
  - In order to add new tests please follow the [pytest](https://docs.pytest.org/en/7.1.x/getting-started.html) recommendations.
- The production code goes inside the `app` folder.
- Inside the `scripts` folder you can find the git hooks files.

## Project commands

The project uses [Makefiles](https://www.gnu.org/software/make/manual/html_node/Introduction.html) to run the most common tasks:

- `help` : Shows this help.
- `local-setup`: Sets up the local environment (e.g. install git hooks).
- `build`: Builds the app.
- `clean`: Cleans the app.
- `run`: Runs the app.
- `install package=XXX`: Installs the package XXX in the app, ex: `make install package=requests`.
- `reformat`: Formats the code.
- `check-typing`: Runs a static analyzer over the code in order to find issues.
- `check-style`: Checks the code style.
- `test`: Run all the tests.

## Packages

This project uses [Poetry](https://python-poetry.org) as the package manager.

To run poetry need the `pyproject.toml` created first and then run `make poetry-init` to install the dependencies.

### Testing

- [pytest](https://docs.pytest.org/en/7.1.x/contents.html): Testing runner.
- [pytest-xdist](https://github.com/pytest-dev/pytest-xdist): Pytest plugin to run the tests in parallel.
- [doublex](https://github.com/davidvilla/python-doublex): Powerful test doubles framework for Python.
- [expects](https://expects.readthedocs.io/en/stable/): An expressive and extensible TDD/BDD assertion library for Python..
- [doublex-expects](https://github.com/jaimegildesagredo/doublex-expects): A matchers library for the Expects assertion librar.

### Code style

- [mypy](https://mypy.readthedocs.io/en/stable/): A static type checker.
- [ruff](https://github.com/astral-sh/ruff): An extremely fast Python linter, written in Rust.