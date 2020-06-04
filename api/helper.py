PREFIX_COMMAND = '!'

def parseMessage(message):
    message = message.text.lower()
    code = message[0]
    rest = message[1:].split()

    return {
        "is_valid": code == PREFIX_COMMAND,
        "command": rest[0], 
        "options": rest[1:], 
    }