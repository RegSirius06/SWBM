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
        scheduler.add_job(main, 'interval', minutes=1)
        now = datetime.datetime.now()
        #time.sleep(3600 * (23 - now.hour) + 60 * (58 - now.minute) + (60 - now.second))
        main()
        scheduler.start()
        while True: pass
