# Accio Sync Tool

> This is a tool for syncing tables between two PostgreSQL databases.

## Usage

```
./run.sh --container-name CONTAINER_NAME
```


## Arguments

- `--container-name CONTAINER_NAME`: The name of the Docker container to run. This argument is required.

## Configuration

The tool uses a configuration file named `config.yml` in the root directory of the project. This file specifies the source and destination databases, as well as the tables to sync.

Example `config.yml` file:

```yaml
source:
  host: localhost
  port: 5432
  database: source_db
  user: postgres
  password: password

destination:
  host: localhost
  port: 5433
  database: destination_db
  user: postgres
  password: password

tables:
  - name: contacts
    primary_key: contact_id
    columns:
      - name: contact_id
      - name: first_name
      - name: last_name
      - name: email
      - name: phone_number
  - name: users
    primary_key: user_id
    columns:
      - name: user_id
      - name: username
      - name: password
