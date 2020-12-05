# Skye bot
Designed to utilitze daily tasks for LINE users.

## Table of Contents:
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Activate and Deactivate Environment](#activate-and-deactivate-environment)
    - [Activate](#activate-environment)
    - [Deactivate](#deactivate-environment)
- [Lint](#lint)
- [Usage](#usage)
    - [Run application](#run-application)
    - [Migrate a model](#migrate-a-model)
    - [Create a superuser](#create-a-superuser)
- [Maintainers](#maintainers)

## Prerequisites
* Python **v3.8.1**
* Pip **v19.3.1**
* Ngrok **v2.3.35**
* Psql **v10.12** - Optional if you will use SQLITE3 instead

## Setup
Ensure you have cloned/pulled the repository to your local. Open terminal from the root repository and run all these commands at once for setup.

1. Create virtual local python environment
    ```sh
    python -m venv env
    ```
2. Activate local environment, you can find a away to do that from this [section](#activate-environment)
2. Install all dependencies.
    ```sh
    pip install -r requirements.txt
    ```
3. Create **.env** in the root repository and add necessary environment variables as follow:
    | Variable              | Optional    | Value                                                       | Default       |
    |-----------------------|-------------|-------------------------------------------------------------|---------------|
    | LINE_CHANNEL_SECRET   | No          | The host of database server                                 |               |
    | LINE_CHANNEL_TOKEN    | No          | The port that used by the host                              |               |
    | DEBUG                 | No          | Either **1** or **0**                                       | **1**         |
    | ALLOWED_HOSTS         | Yes         | List of allowed hosts and separated by comma                | **\***        |
    | DBMS                  | Yes         | Either **SQLITE3** or **POSTGRESQL**                        | **SQLITE3**   |
    | DATABASE_NAME         | Yes         | Targeted database, ensure you have created on your DBMS     |               |
    | DATABASE_USER         | Yes         | User's name to access the database                          |               |
    | DATABASE_PASSWORD     | Yes         | User's password to access the database                      |               |
    | DATABASE_HOST         | Yes         | The host of database server                                 |               |
    | DATABASE_PORT         | Yes         | The port that used by the host                              |               |


## Activate and Deactivate Environment
This section will help you to activate and deacivate local environment through CLI.
* ### Activate Environment
    - Windows
        ```bash
        env\Scripts\activate
        ```
    - Unix
        ```bash
        source env/bin/activate
        ```

* ### Deactivate Environment
    And if you need to close it, then run as easy as run terminated signal:
    - Windows/Unix
        ```bash
        [CTRL + C]
        ```

    or you can close it in gracefully way:
    - Windows/Unix
        ```bash
        deactivate
        ```

## Lint
This repository is linted by ```flake8```. In order to follow the lint's rules, please use ```black``` to format the codes. We already provided all dependencies you need in ```requirements-dev.txt```. You are free to install it through that file or install it manually. Please always run a command below everytime you are going to push it to remote branch:
```bash
$ flake8
```
## Usage
* ### Run application
    Before you follow these instructions, ensure that you already **activated local environment** as follow as this [section](#activate-environment). After that, here are things you need to do.
    1. Run ngrok to make public url 
        ```sh
        ngrok http localhost:8000
        ```
    2. Copy the public url the one with **https** and put it as webhook URL in LINE Bot configuration.
    2. Run the application
        ```sh
        python manage.py runserver
        ```
    3. Exit by triggering a default terminate signal if you already done
        ```sh
        [CTRL + C]
        ```
* ### Migrate a model
    Assume you already started the application. Here are available commands you could use on this project:
    - Make migrations if you edit/create a model
        ```sh
        python manage.py makemigrations
        ```
    - Migrate the model changes you made in database
        ```sh
        python manage.py migrate
        ```
* ### Create a superuser
    Ensure you already started the application before do these steps:
    ```sh
    python manage.py createsuperuser
    ```

## Maintainers
- [Nandhika Prayoga](https://nandhika.netlify.app/)