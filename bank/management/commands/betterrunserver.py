import datetime
import threading

from apscheduler.schedulers.background import BackgroundScheduler
from django.core.management.commands.runserver import Command as RunserverCommand

from bank.models import autotransaction
from server.server import start as start_ngrok, set_link4bot
from tele_bot.start import start as start_tele_bot
from SWBM.settings import PORT, ADDRESS

class Command(RunserverCommand):
    help = 'Better launch than built-in. Launches immediately with autotransactionsrunner, ngrok and telebot (configurable).'

    def add_arguments(self, parser):
        parser.add_argument(
            '--host', 
            type=str, 
            help='Host for server',
            dest='host',
            required=False,
            default=f'{ADDRESS}:{PORT}',
        )
        parser.add_argument(
            '--nongrok',
            action='store_true',
            dest='nongrok',
            help='Run without ngrok',
        )
        parser.add_argument(
            '--noautotransactions',
            action='store_true',
            dest='noautotransactions',
            help='Run without autotransactionsrunner',
        )
        parser.add_argument(
            '--notelebot',
            action='store_true',
            dest='notelebot',
            help='Run without telebot',
        )
        super().add_arguments(parser)

    def handle(self, *args, **options):
        flag = True
        # ngrok
        if not options['nongrok']:
            try:
                host = f'127.0.0.1:{PORT}' if '0.0.0.0' in options['host'] else options['host']
                listener = start_ngrok(host=host)
                self.stdout.write(self.style.SUCCESS('Ngrok server started.'))
                self.stdout.write(self.style.MIGRATE_HEADING(f'Access link: {listener.url()}'))
                set_link4bot(listener.url())
            except ValueError:
                flag = False

        # autotransactions
        if not options['noautotransactions'] and flag:
            def main():
                for i in autotransaction.objects.all():
                    i.create_transactions()
                self.stdout.write(self.style.SUCCESS('Autotransactions done.'))

            self.stdout.write(self.style.MIGRATE_HEADING('Autotransactions runner launched.'))
            scheduler = BackgroundScheduler()
            now = datetime.datetime.now()
            sleep = datetime.timedelta(hours=23 - now.hour, minutes=58 - now.minute, seconds=60 - now.second)
            scheduler.add_job(main, 'interval', hours=24, start_date=now + sleep)
            scheduler.start()

        # telebot
        if not options['notelebot'] and flag:
            telethread = threading.Thread(target=start_tele_bot)
            telethread.start()
            self.stdout.write(self.style.SUCCESS('TeleBot started.'))

        # runserver
        if flag:
            options['addrport'] = options['host']
            super().handle(*args, **options)
