# Nyikes RMS (Records Management System)

Organisation is the driver of great achievements

## Project Overview

Nyikes RMS is a computerized records management system for the Nyikes.

It was created to make it easier for the Nyikes to keep track of it's records relating to it's internal affairs.

## Primary Features

1. Nyikes Officials can create records of:

    + contributions made to the various Nyikes funds
    + expenditures undertaken on the various Nyikes funds

2. Nyikes Members can view records of their contributions

## Getting started

This guide addresses the REST API server component of Nyikes RMS

### Installation

1. Clone the repository

    ```bash
    $ git clone https://github.com/MattAdote/nyikes_rms.git
    ```

2. Navigate to project folder

    ```bash
        $ cd records_mgt
    ```

3. Ensure you're on the develop branch

    ```bash
    $ git checkout develop
    ```

4. Create a python3 virtual environment

    ```bash
    $ python3 -m venv env
    ```

5. Activate the virtual environment

    ```bash
    $ source env/bin/activate
    ```

6. Install requirements

    ```bash
    $ pip install -r requirements.txt
    ```

### Run the app

```bash
$ flask run
```

The api server is now running locally and can be reached on: `http://localhost:5000/`

## Testing

1. Source code unit tests

    + Navigate to app directory
        ```bash
        $ cd app
        ```
    + Execute pytest against the tests directory
        ```bash
        $ pytest tests/
        ```

2. API Endpoints functionality  
    You can use [Postman](https://www.getpostman.com/) to test the endpoints

## Endpoints

This is an evolving section.
The endpoints spec is currently in development

| Request Method       | EndPoint       | Functionality |
| ------------- | ------------- | ---------------
| GET  | `/api/v1/`  | Landing page for backend  |

## Acknowledgements

Nyikwa Kezia
