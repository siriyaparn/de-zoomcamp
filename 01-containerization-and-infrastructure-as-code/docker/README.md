# Introduction to Docker
- Install Docker
- Create a simple data pipeline using Docker

## Ingesting NY Taxi Data to Postgres
Downloading the data
```sh
wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz 
```
### NY Trips Dataset
Dataset:
- https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page
- https://www1.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf

## Running Postgres with Docker
**Windows**

Running Postgres on Windows (note the full path)
```sh
docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v path of working directory:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:13
```

**Linux and MacOS**
```sh
docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:13
```
## CLI for Postgres
`pgcli` is a command-line designed for interacting with PostgreSQL databases on local machine (localhost) or hosted on remote servers.

- Installing `pgcli`
```sh
pip install pgcli
```

- Using `pgcli` to connect to Postgres
```sh
pgcli -h localhost -p 5432 -u root -d ny_taxi
```
## pgAdmin
Running pgAdmin
```sh
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -p 8080:80 \
  dpage/pgadmin4
```
## Running Postgres and pgAdmin together
Create a network
``` sh
docker network create pg-network
```
Run Postgres 
```sh
docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  --network=pg-network \
  --name pg-database \
  postgres:13
```
Run pgAdmin
```sh
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -p 8080:80 \
  --network=pg-network \
  --name pgadmin-2 \
  dpage/pgadmin4
```

## Data ingestion
Running locally
```sh
URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"

python ingest_data.py \
  --user=root \
  --password=root \
  --host=localhost \
  --port=5432 \
  --db=ny_taxi \
  --table_name=yellow_taxi_trips \
  --url=${URL}
```
Build the image
```sh
docker build -t taxi_ingest:v001 .
```
Run with script with Docker
```sh
URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"

docker run -it \
  --network=pg-network \
  taxi_ingest:v001 \
    --user=root \
    --password=root \
    --host=pg-database \
    --port=5432 \
    --db=ny_taxi \
    --table_name=yellow_taxi_trips \
    --url=${URL}
```
