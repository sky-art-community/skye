import json

# Data preparation
# Get list of person in detail, including their birth date
with open('./hbd_list.json') as jsonData:
    hbd_list = json.load(jsonData)["data"]

def __sayHbd(options):
    if options == []:
        return "hbd sokap"
    
    return "hbd {}".format(options[0])

def __nextHbd(options):
    if hbd_list == []:
        return "No one"
    
    return "si {}".format(hbd_list[0]["name"])

# All function that to be called from controller
operators = {
    "hbd": __sayHbd,
    "whoisnext": __nextHbd,
}

def controller(command, options):
    try:
        return operators[command](options)
    except KeyError as e:
        print(e)
        return "the hell is that"