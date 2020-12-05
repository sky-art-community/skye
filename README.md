# Skye Bot
Designed to utilize daily tasks for LINE users.

## Table of Contents:
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Activate and Deactivate Environment](#activate-and-deactivate-environment)
    - [Activate](#activate-environment)
    - [Deactivate](#deactivate-environment)
- [Usage](#usage)
    - [Run application](#run-application)
    - [Migrate a model](#migrate-a-model)
    - [Create a superuser](#create-a-superuser)
- [Maintainers](#maintainers)

## Prerequisites
* Python **v3.8.1**
    - You can download or install python using the following statement:
        - [Windows](https://www.python.org/downloads/windows/)
        - Unix:
            ```sh
            $ sudo apt update
            $ sudo apt install python3
            ```
    - After finished install/download, check the version of your python using this command:
        ```sh
        python3 --version
        ```
* Pip **v19.3.1**
    - You can download or install Pip using the following statement:
        - Windows
            - Download get-pip.py in this [link](https://bootstrap.pypa.io/get-pip.py)
            - run command:
                ```sh
                python get-pip.py
                ```
        - Unix:
            ```sh
            $ sudo apt update
            $ sudo apt install python3-pip
            ```
    - After finished install/download, check the version of your pip using this command:
        ```sh
        pip --version
        ```
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

## Usage
* ### Run application
    Before you follow these instructions, ensure that you already **activated local environment** as follow as this [section](#activate-environment). After that, here are things you need to do.
    1. Migrate all database
        ```sh
        python manage.py migrate
        ```
    2. After migrate, you should run ngrok to make public url 
        ```sh
        ngrok http localhost:8000
        ```
    3. Copy the public url the one with **https** and put it as webhook URL in LINE Bot configuration.
    4. Run the application
        ```sh
        python manage.py runserver
        ```
    5. Exit by triggering a default terminate signal if you already done
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
- [Mutia Rahmatun Husna](https://github.com/mutiarahmatun)
- [Yaumi Alfadha](https://github.com/yaumialfadha)