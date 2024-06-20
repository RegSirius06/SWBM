from django.core.management.base import BaseCommand
from bank.models import autotransaction

class Command(BaseCommand):
    help = 'Creating transactions from autotransactions'

    def handle(self, *args, **options):
        for i in autotransaction.objects.all():
            i.create_transactions()

        self.stdout.write(self.style.SUCCESS('Autotransactions done.'))
