# Skye bot
The official of **Sky Art** bot for LINE.

## Prerequiresites
* Python **v3.8.1**
* Pip **v19.3.1**
* Ngrok **v2.3.35**

## Preparation
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
    LINE_CHANNEL_SECRET=
    LINE_CHANNEL_ACCESS_TOKEN=
    ```
    To fill values for those variables, you need to ask to **the one** who own it or use your own bot.

## Usage
The things that you always do while developing this application.
1. Run ngrok to make public url 
    ```sh
    ngrok http localhost:5000/callback
    ```
2. Copy the public url the one with **https** and put it as webhook URL in LINE Bot configuration.
2. Run
    ```sh
    python app.py
    ```
3. Exit by triggering a default terminate signal
    ```sh
    [CTRL + C]
    ```