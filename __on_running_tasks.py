import json
from datetime import datetime
from linebot.models import TextSendMessage

DATE_FORMAT = '%d-%m-%Y'

class __HbdTask:
    done = []
    undone = []

    def handle(self, x, y):
        x_date = datetime(x['birth_date'], DATE_FORMAT).date()
        y_date = datetime(y['birth_date'], DATE_FORMAT).date()
        x_date = x_date.replace(year=2020)
        y_date = y_date.replace(year=2020)

        return x_date > y_date

    def __init__(self):
        people = []
        with open('./hbd_list.json') as file:
            people = json.load(file)['data']

        sorted_people = sorted(people, self.handle)

        now = datetime.now()
        for person in sorted_people:
            if datetime(person['birth_date'], DATE_FORMAT) >= now:
                self.done.append(person)
            else:
                self.undone.append(person)

    def run(self):
        if self.done == []: return {"should_send_message": False}

        person = self.done[0]
        if datetime(person["birth_date"]).date() == datetime.now().date():
            return {
                "should_send_message": True,
                "to": [

                ],
                "message": "HBD {}!".format(person['nick_name'])
            }



class Tasks:
    tasks = []
    def __init__(self, bot):
        self.tasks.append(__HbdTask())
        self.bot = bot

    def run(self):
        for task in self.tasks:
            response = task.run()
            if response.should_send_message:
                self.bot.multicast(
                    response.to,
                    TextSendMessage(text=response.message)
                )