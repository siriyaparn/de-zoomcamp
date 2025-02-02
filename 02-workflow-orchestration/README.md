# Introduction to Orchestration
Workflow orchestration refers to the automated coordination, management, and execution of tasks within a workflow. It involves organizing and scheduling tasks in a particular sequence to ensure they are executed in the right order and at the right time, based on dependencies, conditions, and requirements.

# What is Kestra?
- Kestra is an all-in-one automation and orchestration platform where it is going to allow you to do things like.
    - ETL/ELT
    - Scheduled & Event-Driven Workflows
    - Batch Data Pipelines
    - Interactive Conditional Inputs
    - API Orchestration
- Kestra gives us flexibility on how we control the workflows with options: no code, low code or full code. 
- Kestra has the topology view which help to visualize what stages are inside of the workflow and how they are going to come together. It is helpful in building complicated and complex pipelines.
- Kestra supports many languages which is useful because while `Pyhton` is a super versatile and useful language but it is not always the right tool for some jobs. Some pipeline might use `Rush` or `C` purely if working with large model and large dataset.
- Kestra allows us to monitor everything and have a good insight into what is going on with these pipelines with Gant view.
- Kestra is enhanced by over 600 plugins.

### What will we cover?
- Introduction to Kestra
- ETL: Extract data and load it to Postgres
- ETL: Extract data and load it to Google Cloud
- Parammeterzing Execution
- Scheduling and Backfills
- Install Kestra on the Cloud and sync your Flows with Git

## Build Data Pipelines with Kestra
### Resources
- [Quickstart](https://kestra.io/docs/getting-started/quickstart)
- [Install Kestra with Docker Compose](https://kestra.io/docs/installation/docker-compose)
- [Tutorial](https://kestra.io/docs/getting-started/tutorial)
