from django.core.management.base import BaseCommand

from tele_bot.start import start

class Command(BaseCommand):
    help = 'Starrting TeleBot'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('TeleBot started.'))
        start()
        self.stdout.write(self.style.ERROR('TeleBot stopped.'))
