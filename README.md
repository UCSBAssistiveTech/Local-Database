# Local-Database
Backend Local Mockup

# LocalStack
We're using localstack to simulate AWS infrastructure we may be using later. LocalStack emulates an AWS-like environment so we can practice creating these kinds of processes then apply them later.

## Prerequisites 

### Python
- we probably gonna use Python so have that I assume u have it if not download!!!, and get pip or whatver package manager u like

### Boto3 / AWS SDK for Python
- This allows us to interact with AWS services from within our Python code using `pip install boto3` unless u use a different package manager then u can figure it out

### Docker 
- Install Docker [Install Docker](https://www.docker.com/get-started/) 
- Very useful tool, read about it, it is good if you wanna be a SWE
- We're gonna use it to run LocalStack within a container on our machines

### Docker Compose
- This should be included in the base Docker download ^
- Docker Compose helps us orchestrate more than one container and lots of useful config all in one file (docker-compose.yaml)


## Quick Start

- Go to the directory these files are in on your computer 
- Open up your terminal
- `docker compose up` will automatically find the file named docker-compose.yaml in the current working directory and then do all of that stuff for u
- `docker compose down` takes it down, make sure to do this whenever you're done since it uses up resources on your machine
