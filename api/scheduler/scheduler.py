
from apscheduler.schedulers.background import BackgroundScheduler

# Local schedules
from api.scheduler.schedules import update_free_games

class ScheduledTask:
    def __init__(self, function, seconds = 0, minutes = 0, hours = 0):
        self.__function = function
        self.__callback_delay = {
            "seconds": seconds,
            "minutes": minutes,
            "hours": hours,
        }

    def get_function(self):
        return self.__function

    def get_delay(self):
        return self.__callback_delay

# Set all scheduled tasks
SCHEDULED_TASKS = [
    ScheduledTask(update_free_games.update_free_games, hours=1),
]

# Start all scheduled tasks
def start_scheduler():
    scheduler = BackgroundScheduler()
    for task in SCHEDULED_TASKS:
        interval_delay = task.get_delay()
        scheduler.add_job(
            task.get_function(),
            'interval',
            seconds=interval_delay['seconds'],
            minutes=interval_delay['minutes'],
            hours=interval_delay['hours']
        )
    scheduler.start()