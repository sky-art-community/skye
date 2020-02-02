import json
from datetime import datetime
from linebot.models import TextSendMessage
from functools import cmp_to_key
import pydash
from pprint import pprint

DATE_FORMAT = '%d-%m-%Y'

class HbdTask:
    done = []
    undone = []

    def handle(self, x, y):
        x_date = datetime.strptime(x['birth_date'], DATE_FORMAT).date().replace(year=2020)
        y_date = datetime.strptime(y['birth_date'], DATE_FORMAT).date().replace(year=2020)

        if x_date >= y_date:
            return 1
        return -1

    def __init__(self):
        people = []
        with open('./hbd_list.json') as file:
            people = json.load(file)['data']

        sorted_people = sorted(people, key=cmp_to_key(self.handle))

        now = datetime.now().date().replace(year=2020)
        for person in sorted_people:
            person_date = datetime.strptime(person['birth_date'], DATE_FORMAT).date().replace(year=2020)
            if person_date >= now:
                self.undone.append(person)
            else:
                self.done.append(person)

    def run(self):
        if self.done == []: return {"should_send_message": False}

        person = self.undone[0]
        person_date = datetime.strptime(person["birth_date"], DATE_FORMAT).date().replace(year=2020)
        now = datetime.now().date().replace(year=2020)

        # print(person_date)
        # print(now)
        # print()

        if person_date == now:
            self.done.append(person)
            self.undone = pydash.arrays.pull(self.undone, person)

            return {
                "should_send_message": True,
                "to": [
                    "U368963b7b7a0695f94fd9eb0c79b4f38"
                ],
                "message": "HBD {}!".format(person['nick_name'])
            }
        
        return {"should_send_message": False}



class Tasks:
    tasks = []
    def __init__(self, bot):
        self.tasks.append(HbdTask())
        self.bot = bot

    def run(self):
        for task in self.tasks:
            response = task.run()
            if response["should_send_message"]:
                self.bot.multicast(
                    response['to'],
                    TextSendMessage(text=response["message"])
                )