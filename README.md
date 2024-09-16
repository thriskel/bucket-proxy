# Project Name

simple r/w FastAPI S3 proxy project.

The project works as a proxy for creating and obtaining objects to/from a S3 bucket.

## Table of Contents

- Requirements
- Installation
- Usage
- API Endpoints
- Technologies

## Requirements

- Docker

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/thriskel/bucket-proxy.git
    cd bucket-proxy
    ```

2. Create a ***.env*** file with the following variables:
    ```bash
    AWS_ACCESS_KEY_ID=<your-aws-access-key>
    AWS_SECRET_ACCESS_KEY=<your-aws-secret-access-key>
    AWS_DEFAULT_REGION=<the-region-of-your-s3>
    ```

3. Start docker compose:
    ```bash
    docker compose up --build
    ```

## Usage

You can access this project endpoints through localhost using 8000 port once the docker containers are up and running.

This project has the following Swagger urls:
/docs
/redoc

It is important to fill the .env file once you clone the repo to allow communication to the desired AWS account.

## API Endpoints

- /buckets/<bucket_name>/objects/<object_name> ['POST', 'GET']

## Technologies

- FastAPI
- Boto3
- asyncio
- Docker