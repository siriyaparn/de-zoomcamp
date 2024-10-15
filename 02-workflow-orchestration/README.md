# Intro to Orchestration
Workflow orchestration refers to the automated coordination, management, and execution of tasks within a workflow. It involves organizing and scheduling tasks in a particular sequence to ensure they are executed in the right order and at the right time, based on dependencies, conditions, and requirements.

### A good orchestrator handles ..
- `Workflow management`: define schedule, manage workflows efficiently, ensure tasks are executed in the right order and manage dependencies
- `Automation`: make sure that the orchestration solution is good at automation
- `Error handling`: come up with build-in solutions for handling errors, conditional logic branching, retrying failed tasks
- `Recovery`: need to be a way to backfill, a way to recover lost data
- `Monitoring`, alerting: send a notification if a pipeline or if those retries do to happen
- `Resource optimization`: optimize the best route for the execution
- `Observability`: have visibility into every part of the data pipeline 
- `Debugging`: part of observability, debug data pipelines easily
- `Compliance, auduting`: help with compliance or auditing

### A good orchestrator priortizes ..
- `Flow state`: ensure that tasks are completed seamlessly without unnecessary interruptions
- `Feedback loops`: ensure that users or systems are informed about progress, errors, or successes as quickly as possible
- `Cognitive load`: reduce the effort required to operate or monitor the orchestrated processes

# Intro to Mage
### What is Mage?
Mage is an open-source pipeline tool for orchestrating, transforming, and integrting data

**Mage accelerates pipeline development**
- Hybrid environment
  - Use GUI for interactive development
  - Use blocks as testable, reusable pieces of code
- Improved DevEx
  - Code and test in parallel
  - Reduce your dependencies, switch tools less, be efficient

**Engineering best-practices built-in**
- In-line testing and debugging
  - Familiar, notebook-style format
- Fully-featured observability
  - Transformation in one place: dbt models, streaming
- Dry principles
  - No more DAGs with duplicate functions
 
### The core concept in Mage
**Projects**
- A project forms the basis for all the work you can do in Mage— you can think of it like a GitHub repo.
- It contains the code for all of your pipelines, blocks, and other assets.
- A Mage instance has one or more projects.

**Pipelines**
- A pipeline is a workflow that executes some data operation— maybe extracting, transforming, and loading data from an API. They’re also called DAGs on other platforms.
- In Mage, pipelines can contain Blocks (written in SQL, Python, or R) and charts.
- Each pipeline is represented by a YAML file in the ``pipelines`` folder of your project.

**Blocks**
- A block is a file that can be executed independently or within a pipeline. 
- Together, blocks form Directed Acyclic Graphs (DAGs), which we call pipelines.
- A block won’t start running in a pipeline until all its upstream dependencies are met.
- Blocks are reusable, atomic pieces of code that perform certain actions.
- Changing one block will change it everywhere it’s used, but don’t worry, it’s easy to detach blocks to separate instances if necessary.
- Blocks can be used to perform a variety of actions, from simple data transformations to complex machine learning models.
