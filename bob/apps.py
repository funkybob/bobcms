
from django.apps import apps
from django.db.signals import pre_save
from django.utils import timezone


def update_edited(sender, instance=None, **kwargs):
    from .models import Base
    if isinstance(instance, Base):
        instance.edited = timezone.now()


class BobConfig(apps.AppConfig):
    name = 'bob_cms'

    def ready(self):
        pre_save.connect(update_edited)
