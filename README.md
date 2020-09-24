# Skye bot
The official of **Sky Art** LINE bot.

## Table of Contents:
- [Prerequisites](#prerequisites)
- [Setup](#setup)
    - [Windows](#windows)
- [Usage](#usage)
    - [Run application](#run-application)
    - [Migrate a model](#migrate-a-model)
    - [Create a superuser](#create-a-superuser)
- [Maintaners](#maintainers)
- [Acknowledgements](#acknowledgements)

## Prerequisites
* Python **v3.8.1**
* Pip **v19.3.1**
* Ngrok **v2.3.35**
* Psql **v10.12**

## Setup
Ensure you have cloned/pulled the repository to your local. Open terminal in the root repository and run all these commands.

### Windows
1. Create virtual local python environment
    ```sh
    python -m venv env
    ```
2. Activate local environment we just created.
    ```sh
    env\Scripts\activate.bat
    ```
3. Install all dependencies.
    ```sh
    pip install -r requirements.txt
    ```
4. Create **.env** in the root repository and add environment variables as follow:
    ```sh
    DBMS=
    DATABASE_NAME=
    DATABASE_USER=
    DATABASE_PASSWORD=
    DATABASE_HOST=
    DATABASE_PORT=

    LINE_CHANNEL_SECRET=
    LINE_CHANNEL_ACCESS_TOKEN=
    ```
    To fill values for those variables, you need to ask to **the one** who own it or use your own bot.
    
    For DBMS, here are the available DBMS you could use:
    1. PostgreSQL
        ```sh
        DBMS=POSTGRESQL
        ```
    2. Sqlite (Django built-in)
        ```sh
        DBMS=SQLITE
        ```


## Usage
* ### Run application
    Before you follow these instructions, ensure that you already **activated local environment**. After that, here are things you need to do.
    1. Run ngrok to make public url 
        ```sh
        ngrok http localhost:8000
        ```
    2. Copy the public url the one with **https** and put it as webhook URL in LINE Bot configuration.
    2. Run the application
        ```sh
        python manage.py runserver
        ```
    3. Exit by triggering a default terminate signal if you done
        ```sh
        [CTRL + C]
        ```
* ### Migrate a model
    Assume you already started the application. Here are available commands you could use on this project:
    - Make migrations if you edit/create a model
        ```sh
        python manage.py makemigrations
        ```
    - Migrate
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

## Acknowledgements
- LINE
- Django, python, and all libraries
- Heroku