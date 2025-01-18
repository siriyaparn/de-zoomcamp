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