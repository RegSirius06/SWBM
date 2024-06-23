import datetime
import time

from apscheduler.schedulers.background import BackgroundScheduler
from django.core.management.base import BaseCommand

from bank.models import autotransaction

class Command(BaseCommand):
    help = 'Creating transactions from autotransactions automatically'

    def handle(self, *args, **options):
        def main():
            for i in autotransaction.objects.all():
                i.create_transactions()

            self.stdout.write(self.style.SUCCESS('Autotransactions done.'))

        self.stdout.write(self.style.MIGRATE_HEADING('Autotransactions runner launched.'))
        scheduler = BackgroundScheduler()
        now = datetime.datetime.now()
        sleep = datetime.timedelta(hours=23 - now.hour, minutes=58 - now.minute, seconds=60 - now.second)
        scheduler.add_job(main, 'interval', hours=24, start_date=now + sleep)
        main()
        scheduler.start()
        while True: pass
