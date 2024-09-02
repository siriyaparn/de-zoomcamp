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
`pgcli` is a command-line designed for interacting with PostgreSQL databases.

Installing `pgcli`
```sh
pip install pgcli
```

Using `pgcli` to connect to Postgres
```
pgcli -h localhost -p 5432 -u root -d ny_taxi
```

