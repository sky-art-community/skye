
from apscheduler.schedulers.background import BackgroundScheduler

# Local schedules
from api.scheduler.schedules import update_free_games

class ScheduledTask:
    def __init__(
        self,
        function,
        seconds = 0,
        minutes = 0,
        hours = 0,
        call_at_first = False,
    ):
        if call_at_first:
            function()

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
<<<<<<< HEAD
    ScheduledTask(update_free_games.update_free_games, hours=1, call_at_first=True),
=======
    # ScheduledTask(update_free_games.update_free_games, hours=1, call_at_first=True),
>>>>>>> 4b60e6aa863747fda12ff6da0e0c6f4fffdbadd9
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