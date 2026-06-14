from django.apps import AppConfig
from django.core.signals import setting_changed


class BankConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bank'

    def ready(self):
        from bank import signals
        setting_changed.connect(signals.create_or_refresh_qr)
