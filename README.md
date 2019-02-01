# Nyikes RMS (Records Management System)

Organisation is the driver of great achievements

[![Build Status](https://travis-ci.com/MattAdote/nyikes_rms.svg?token=Ry3JQbWPQTsKSQdKfwjr&branch=develop)](https://travis-ci.com/MattAdote/nyikes_rms)

[![Coverage Status](https://coveralls.io/repos/github/MattAdote/nyikes_rms/badge.svg?branch=develop)](https://coveralls.io/github/MattAdote/nyikes_rms?branch=develop)

## Project Overview

Nyikes RMS is a computerized records management system for the Nyikes.

It was created to make it easier for the Nyikes to keep track of it's records relating to it's internal affairs.

## Primary Features

1. Nyikes Officials can create records of:

    + contributions made to the various Nyikes funds
    + expenditures undertaken on the various Nyikes funds

2. Nyikes Members can view records of their contributions

## Getting started

This guide addresses the REST API server component of Nyikes RMS.

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

## Heroku

Nyikes RMS is hosted on heroku as well at `https://nyikes-rms.herokuapp.com/` i.e. [here](https://nyikes-rms.herokuapp.com/)

As no content has been configured yet to be displayed, you will see a Not found message i.e.
> **Not Found**
>
> The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.

Do not be alarmed. Something shall be setup in due time.

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
    You can use [Postman](https://www.getpostman.com/) to test the endpoints.

## Endpoints

This is an evolving section.
The endpoints spec is currently in development.

The endpoint prefix is `api/v1`

The full url to access an endpoint takes the form:
> [server_url] / [endpoint_prefix] / [endpoint]

i.e if on localhost, the url is `http://localhost:5000/api/v1/[endpoint]`

or if on heroku, the url is `https://nyikes-rms.herokuapp.com/api/v1/[endpoint]`

**Note** :  the [endpoint] provides the slash '/' after the [endpoint_prefix] thus,
            the [endpoint] = / means the root endpoint with no need for two slashes after
            the [endpoint_prefix]

### Available endpoints

| Request Method       | EndPoint       | Functionality |
| ------------- | ------------- | ---------------
| GET  | `/`  | "Landing page" for the REST API server |

## Acknowledgements

Nyikwa Kezia
