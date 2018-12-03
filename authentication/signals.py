from django.contrib.auth.models import User
from django.db.models import signals
from django.dispatch import receiver

from authentication.models import UserGUISettings


@receiver(signals.post_save, sender=User)
def create_user_gui_settings(instance, created, **kwargs):
    """Creates a UserGUISettings item on user create
    """
    if created:
        UserGUISettings.objects.create(user=instance)
