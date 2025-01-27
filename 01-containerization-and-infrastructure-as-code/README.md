# Introduction to Docker
Docker is an open-source platform that allows developers to easily create, deploy, and run applications in containers. Containers are lightweight, portable, and self-sufficient environments that allow applications to run consistently across different environments.
- Install Docker
- Create a simple data pipeline using Docker

## Docker command
```sh
docker run hello-world

# -it: run iterative mode
docker run -it ubuntu bash  

docker run -it python:3.9
docker run -it --entrypoint=bash python:3.9

# build an image called taxi-ingest:v001
docker build -t taxi-ingest:v001 .

docker run -it test:pandas
```

## Ingesting NY Taxi Data to Postgres
### Postgres
Postgres is a versatile database that is designed for transactional purposes rather than analytics. Despite this, it is powerful and sometimes employed as a data warehouse solution.

Downloading the data
```sh
wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz 
```
To extract the file
```sh
gzip -d yellow_tripdata_2021-01.csv.gz
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

- Check with tables
```sh
/dt
```

## pgAdmin
It is not convenient to use pgcli for data exploration and querying. Instead, we will use pgAdmin, the standard graphical tool for postgres. We can run it with docker. However, this docker container cannot access the postgres container. We need to link them by creating a network.

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