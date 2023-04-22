import sys
import psycopg2
import psycopg2.extras
import yaml

# load the configuration file
with open("config.yml", "r") as f:
    config = yaml.safe_load(f)

# connect to the source and destination databases
source_conn = psycopg2.connect(**config["source"])
destination_conn = psycopg2.connect(**config["destination"])

# set up cursors for both databases
source_cursor = source_conn.cursor()
destination_cursor = destination_conn.cursor()

# retrieve the list of tables to sync from the configuration file
tables = config["tables"]

for table in tables:
    # get the primary key for the current table
    primary_key = table.get(
        "primary_key", "id"
    )  # get the column names for the current table
    columns = table["columns"]
    column_names = [column["name"] for column in columns]
    # add the primary key to the column names if it's not already present
    if primary_key not in column_names:
        column_names.append(primary_key)
    # generate the SELECT query for the source database
    select_query = f"SELECT {', '.join(column_names)} FROM {table['name']}"
    # execute the SELECT query on the source database
    source_cursor.execute(select_query)
    # retrieve the rows from the source database
    source_rows = source_cursor.fetchall()
    # generate the INSERT/UPDATE query for the destination database
    insert_query = f"INSERT INTO {table['name']} ({', '.join(column_names)}) VALUES %s ON CONFLICT ({primary_key}) DO UPDATE SET {', '.join([f'{col} = EXCLUDED.{col}' for col in column_names if col != primary_key])}"
    # generate the values to insert/update
    new_records = [tuple(row) for row in source_rows]
    # execute the INSERT/UPDATE query on the destination database
    psycopg2.extras.execute_values(destination_cursor, insert_query, new_records)

# commit the changes to the destination database and close the connections
destination_conn.commit()
destination_conn.close()
source_conn.close()
print(
    f"tables --> ( {', '.join(table['name'] for table in tables)} ). Synced successfully!"
)
sys.exit(0)
