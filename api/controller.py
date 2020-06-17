def status(options):
    return "Yo I'm here"


def __showImg(options):
    pass


# All function will be called from controller
commands = {
    "status": status,
}

def controller(command, options):
    try:
        return commands[command](options)
    except KeyError as e:
        print(e)
        return "Sorry, can't recognize your command".format(command)