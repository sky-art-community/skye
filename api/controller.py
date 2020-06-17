def status(options):
    return "Yo I'm here"


def show(options):
    # TODO: Implement show image
    pass


# All function will be called from controller
commands = {
    "status": status,
    "show": show,
    "sh": show,
}

def controller(command, options):
    try:
        return commands[command](options)
    except KeyError as e:
        print(e)
        return "Sorry, can't recognize your command".format(command)