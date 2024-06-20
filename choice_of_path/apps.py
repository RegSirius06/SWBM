import os

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
        scheduler.add_job(main, 'interval', hours=12)
        main()
        scheduler.start()
