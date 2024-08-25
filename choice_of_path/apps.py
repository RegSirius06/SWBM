import os
import datetime

from django.apps import AppConfig
from apscheduler.schedulers.background import BackgroundScheduler

from utils.db_copier import destination_directory, main

class ChoiceOfPathConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'choice_of_path'

    def ready(self) -> None:
        if not os.path.isdir(destination_directory):
            os.makedirs(destination_directory)
        scheduler = BackgroundScheduler()
        now = datetime.datetime.now()
        sleep = datetime.timedelta(hours=(23 - now.hour) % 12, minutes=58 - now.minute, seconds=60 - now.second)
        scheduler.add_job(main, 'interval', hours=12, start_date=now + sleep)
        scheduler.start()
