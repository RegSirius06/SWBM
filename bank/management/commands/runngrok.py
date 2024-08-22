from django.core.management.base import BaseCommand

from server.server import start, set_link4bot
from SWBM.settings import PORT, ADDRESS

class Command(BaseCommand):
    help = 'Starting ngrok'

    def add_arguments(self, parser):
        parser.add_argument(
            '--host', 
            type=str,
            dest='host',
            help='Localhost for ngrok',
            required=False,
            default=f'{ADDRESS}:{PORT}' if ADDRESS != '0.0.0.0' else f'127.0.0.1:{PORT}',
        )

    def handle(self, *args, **options):
        listener = start(host=options['host'])
        self.stdout.write(self.style.SUCCESS('Server started.'))
        self.stdout.write(self.style.MIGRATE_HEADING(f'Access link: {listener.url()}'))
        set_link4bot(listener.url())

        # Keep the listener alive
        try:
            while True:
                pass
        except KeyboardInterrupt:
            self.stdout.write(self.style.ERROR('Closing server.'))
