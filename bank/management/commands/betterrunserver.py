import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from django.core.management.commands.runserver import Command as RunserverCommand

from bank.models import autotransaction
from SWBM.settings import PORT, ADDRESS


class Command(RunserverCommand):
    help = (
        'Improved runserver command. '
        'Launches the server together with the autotransactions runner (configurable).'
    )

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
            '--noautotransactions',
            action='store_true',
            dest='noautotransactions',
            help='Run without autotransactions runner',
        )
        super().add_arguments(parser)

    def handle(self, *args, **options):
        flag = True

        if not options['noautotransactions'] and flag:
            def run_autotransactions():
                for trans in autotransaction.objects.all():
                    trans.create_transactions()
                self.stdout.write(self.style.SUCCESS('Autotransactions done.'))

            self.stdout.write(self.style.MIGRATE_HEADING('Autotransactions runner launched.'))
            scheduler = BackgroundScheduler()
            now = datetime.datetime.now()
            sleep = datetime.timedelta(
                hours=23 - now.hour,
                minutes=58 - now.minute,
                seconds=60 - now.second,
            )
            scheduler.add_job(run_autotransactions, 'interval',
                              hours=24,
                              start_date=now + sleep)
            scheduler.start()

        options['addrport'] = options['host']
        super().handle(*args, **options)
