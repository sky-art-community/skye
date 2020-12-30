# Programmer's guide
To synchronize every different works from different developer, this manual standarize every common work in this repository in hope will help you to minimize the variety from others. 

# Table of Contents
- [Code Structure](#code-structure)
- [Add command](#add-command)
- [Sources](#sources)
- [Troubleshootings](#troubleshootings)

# Code structure
```
[Root]
├── api
│   ├── commons.py                  <- Common modules that commonly used by command function
│   ├── controller.py               <- Where all commands exist
│   ├── helper.py                   <- Common modules that commonly used by any modules on api folder
│   ├── models.py                   <- Define models/table to store information for a long-time period
│   ├── tests.py                    <- All unit tests of commands (on controller.py)
│   ├── urls.py                     <- Define endpoint to access the bot API (only one)
│   ├── views.py                    <- Parse incoming message from LINE
│   ├── ...                         <- For the rest files, you should go further look at Django documentation
│
├── skye                            <- Configuration files
│   ├── settings.py                 <- Auth bot, Allowed host, secret key, database, timezone, etc
│   ├── urls.py                     <- Root urls, this will forward to api/urls.py
│   ├── ...                         <- For the rest files, you should go further look at Django documentation
│
├── .env                            <- Local variables
├── env                             <- Local environment, where all installed packages will be stored
├── requirements.txt                <- All required packages are defined in here
```

# Add command
Add command must be done on ```controller.py``` by registering the command name and implement the actual functionality. This is an example registering command to call hello world functionality:
1. Register the command name and the related function to call, please don't let the name is conflict with others.
    ```py
    # ... rest codes

    commands = {
        "status": status,
        "info": info,

        # ... rest codes

        "helloworld": helloworld_fun,
    }

    # ... rest codes
    ```
2. Now comes to implement the function, the function will receive ```event``` and ```options``` and return kind of LINE bot message. For example we call command as following below via LINE chat to the bot
    ```bash
    !helloworld nandhika
    ```
    So it will call ```helloworld_fun``` function, because we map as like that. And the function also will receive an option as list.
    ```py
    from linebot.models import (
        TextSendMessage,
    )

    # ... rest codes

    def helloworld_fun(event, options):
        # event     -> Event LINE bot
        # options   -> In above scenario, will be ['nandhika']
        if len(options) > 0:
            return TextSendMessage(text = "Hello world by " + optionts[0])

        # Return kind of LINE bot message, please take a look at the offical LINE bot documentation which I provided below
        return TextSendMessage(text = "Hello world")
    ```
Event is defined as the event of message and with event you can get an interesting data, such as group id, user id, timestamp of chat, etc. The data structure of event is defined at the offical LINE bot SDK. So it will not be covered a full detail of structure of event in here, please go further reading at their repository.  

You should be noticed that ```TextSendMessage``` is not the only one to be returned, there are some variety with different purposes, such as ```ImageSendMessage```, ```VideoSendMessage```, ```AudioSendMessage```, etc. Please go further reading at the offical that I provided in [here](#sources)
# Sources
- https://github.com/line/line-bot-sdk-python - LINE bot SDK documentation

# Troubleshootings
Please write down the troubleshootings you ever face in here to help developers to contribute without any problems.

