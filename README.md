# Svitbo Backend

## How to Start

Copy the example of the environment file and adjust values for your needs.
These values are used only in the testing purposes.

```shell
cp .env.example .env
```

Start local MariaDB, Adminer (simple UI for the DB) and backend instances using Docker Compose functionality:

```shell
# This can take some time on the first run
docker compose up -d
```

Now your backend is accessible under the `http://localhost:9000` address.

Or you can connect to your local MariaDB instance using Adminer Web UI:

- Open the `http://localhost:8090` from your browser
- Fill all connection fields:
  - System: `MySQL`
  - Server: `mariadb:3307` # Hostname is resolved by the Docker inner-network
  - Username: `<MARIADB_USER-value-from-.env-file>`
  - Password: `<MARIADB_PASSWORD-value-from-.env-file>`
  - Database: `<MARIADB_DATABASE-value-from-.env-file>`
- After pressing the `Login` button, you should see another page with Adminer interface
