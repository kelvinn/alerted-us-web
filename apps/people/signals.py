import os
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from rest_framework.authtoken.models import Token
from apps.people.models import Location, LocationHistory
from apps.people.tasks import save_location_history, run_alertdb_search

AUTH_USER_MODEL = settings.AUTH_USER_MODEL  # This is a bit of a hack for App registry loading

@receiver(post_save, sender=AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(post_save, sender=Location)
def archive_location(sender, instance=None, created=False, **kwargs):
    # Probably worthwhile making this as a background task at some point
    if instance.source == "current":
        save_location_history.delay(instance)
        run_alertdb_search.delay(instance)  # TODO make this work?

