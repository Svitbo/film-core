# 🦭 Svitbo Core

The core part of the Svitbo project that consists of the following services:

- FastAPI backend
- MariaDB data layer
- Adminer DB manager (optional)

Suits well with the [Svitbo frontend](https://github.com/Svitbo/film-frontend).

## Requirements

The list of requirements needed to bootstrap the backend:

- Python 3.8+
- Docker with Compose plugin
- Make

## Environments

Currently, the core part supports two environments:

- `prod`:
  - Starts the FastAPI service without publishing any ports
  - Starts the MariaDB service without publishing any ports
- `dev`:
  - Exposes FastAPI service on port `9000`
  - Exposes MariaDB service on port `4472`
  - Exposes Adminer service on port `9292`

## How to Start

Copy an example of the environment file and adjust values based on your needs:

```shell
cp .env.example .env
```

Start local service instances using Docker Compose functionality:

```shell
# This can take some time on the first run
make core-apply-dev

# Or, if you want to simulate prod environment:
make core-apply-prod
```

Now you can reach FastAPI backend targeting the `http://localhost:9000` address.

Or you can connect to your local MariaDB instance using Adminer Web UI:

- Open the `http://localhost:9292` from your browser
- Fill all connection fields:
  - System: `MySQL`
  - Server: `mariadb`
  - Username: `<MARIADB_USER-value-from-dotenv-file>`
  - Password: `<MARIADB_PASSWORD-value-from-dotenv-file>`
  - Database: `<MARIADB_DATABASE-value-from-dotenv-file>`

## Supported Make Targets

### Environment-Specific

| Target              | Action                                                                                           |
| ------------------- | ------------------------------------------------------------------------------------------------ |
| core-apply-${env}   | Turns up all the services with environment-specific configurations                               |
| core-destroy-${env} | Turns off all the services. Additionally, prune the MariaDB data volume in the `dev` environment |

### Project-Specific

| Target    | Action                                                                      |
| --------- | --------------------------------------------------------------------------- |
| venv      | Generates Python's virtual environment and installs all dependency packages |
| core-logs | Attaches terminal to the Docker Compose logs of all started services        |
