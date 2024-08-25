import os

from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from django.contrib.auth.models import User

from bank.models import account
from SWBM.settings import DATABASES

class Command(BaseCommand):
    help = 'It is initializes the database.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            type=str,
            help='Admin\'s email.',
            dest='email',
            required=False,
            default=''
        )
        parser.add_argument(
            '--password',
            type=str,
            help='Admin\'s password.',
            dest='password',
            required=False,
            default='admin'
        )

    def handle(self, *args, **options):
        try:
            if os.path.exists(DATABASES["default"]["NAME"]):
                raise CommandError("Database already exists!")

            call_command('makemigrations')
            call_command('migrate')

            email = options['email']
            username = 'admin'
            password = options['password']

            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )

            admin_account = account()
            admin_account.user = user
            admin_account.first_name = "BANK"
            admin_account.middle_name = "BANK"
            admin_account.last_name = "Admin"
            admin_account.save()
        except CommandError as e:
            self.stderr.write(e)
