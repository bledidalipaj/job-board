import datetime

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Job

JOB_DURATION_DAYS = 30


@receiver(post_save, sender=Job)
def set_expiration_date(sender, instance, created, **kargs):
    if created:
        instance.expires = instance.created + datetime.timedelta(JOB_DURATION_DAYS)
        instance.save()
