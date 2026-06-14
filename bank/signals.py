from django.db.models.signals import post_save
from django.dispatch import receiver
from bank.models import account
from utils.qrgen import generate_qr_for_user

@receiver(post_save, sender=account)
def create_or_refresh_qr(sender, instance, created, **kwargs):
    if created:
        instance.qr_image = generate_qr_for_user(instance)
        instance.save()