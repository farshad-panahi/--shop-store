from django.db.models.signals import post_save

from django.dispatch import receiver


from django.conf import settings
from .models import Customer


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_customer_after_user_creation(sender, instance, created, **kw):
    if created:
        Customer.objects.create(user=instance)
