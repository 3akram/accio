
FROM postgres:13.4

RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    pip3 install psycopg2-binary && \
    pip3 install PyYAML

WORKDIR /app

# Copy the scirpt
COPY sync_db_tables.py .

CMD ["python3", "sync_db_tables.py"]
