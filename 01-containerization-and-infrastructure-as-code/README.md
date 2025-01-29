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

## Data ingestion
- Converting the Jupyter notebook to a Python script
- Parametrizing the script with argparse
- Dockerizing the ingestion script

Run locally
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
Or build the image from Dockerfile
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

## Running Postgres and pgAdmin with Docker-Compose
### Docker-Compose
Docker-Compose is a powerful tool that makes it easy to define and run multi-container Docker applications, simplifying the process of development, testing, and deployment. It allows developers to define all the services and dependencies of an application in a single file, and then start, stop, and manage those services with simple commands. Docker-Compose also allows developers to define networks and volumes that can be shared between services. The docker-compose.yml file is a YAML file that defines the services, networks, and volumes needed for the application.

To connect two Docker containers together, we create a Docker network. However, we can also connect two Docker containers without creating a network by using a YAML file.

Run Docker-Compose
```sh
docker-compose up
```

Run in detached mode
```sh
docker-compose up -d
```

Shut Docker-Compose down
```sh
docker-compose down
```

# Introduction to Terraform
Terraform is an open-source Infrastructure-as-Code (IaC) tool developed by HashiCorp. It is used for provisioning, managing, and automating infrastructure resources such as servers, databases, and networking components across various cloud providers and on-premise environments. 

**What is IaC?**
- Infrastructure-as-Code
- build, change, and manage your infrastructure in a safe, consistent, and repeatable way by defining resource configurations that you can version, reuse, and share.

**Some advantages**
- Infrastructure lifecycle management
- Version control commits
- Very useful for stack-based deployments, and with cloud providers such as AWS, GCP, Azure, K8S…
- State-based approach to track resource changes throughout deployments

**Files**

- `main.tf`
- `variables.tf`
- Optional: `resources.tf`, `output.tf`
- `.tfstate`

**Declarations**

- `terraform`: configure basic Terraform settings to provision your infrastructure
  - `required_version`: minimum Terraform version to apply to your configuration
  - `backend`: stores Terraform's "state" snapshots, to map real-world resources to your configuration.
    - `local`: stores state file locally as terraform.tfstate
  - `required_providers`: specifies the providers required by the current module
- `provider`
  - adds a set of resource types and/or data sources that Terraform can manage
  - The Terraform Registry is the main directory of publicly available providers from most major infrastructure platforms.
- `resource`
 - blocks to define components of your infrastructure
 - Project modules/resources: google_storage_bucket, google_bigquery_dataset, google_bigquery_table
- `variable` & `locals`
  - runtime arguments and constants

## Terraform command
Initialize, configure the backend, install plugins/providers, check out an existing configuration from a version control
```sh
terraform init
```

Match and preview local changes against a remote state, and proposes an Execution Plan
```sh
terraform plan
```

Ask for approval to the proposed plan, and applies changes 
```sh
terraform apply
```

Remove your stack 
```sh
terraform destroy
```

# Google Cloud Platform (GCP) Overview
### Initial Setup
For this course, we'll use a free version (upto EUR 300 credits)
1. Create an account with your Google email ID
2. Setup your first project if you haven't already
3. Setup service account & authentication for this project
   -  Grant Viewer role to begin with.
   - Download service-account-keys (.json) for auth
5. Download SDK for local setup
6. Set environment variable to point to your downloaded GCP keys:
  ```sh
  export GOOGLE_APPLICATION_CREDENTIALS="<path/to/your/service-account-authkeys>.json"
  # Refresh token/session, and verify authentication
  gcloud auth application-default login
  ```

### Setup for Access
1. IAM Roles for Service account:
   - Go to the IAM section of IAM & Admin https://console.cloud.google.com/iam-admin/iam
   - Click the Edit principal icon for your service account
   - Add these roles in addition to Viewer : Storage Admin + Storage Object Admin + BigQuery Admin
2. Enable these APIs for your project:
   - https://console.cloud.google.com/apis/library/iam.googleapis.com
   - https://console.cloud.google.com/apis/library/iamcredentials.googleapis.com
3. Ensure `GOOGLE_APPLICATION_CREDENTIALS env-var` is set

   ```sh
   export GOOGLE_APPLICATION_CREDENTIALS="<path/to/your/service-account-authkeys>.json"
   ```