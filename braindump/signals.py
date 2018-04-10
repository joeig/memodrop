from django.db.models import signals
from django.dispatch import receiver

from braindump.models import CardPlacement
from cards.models import Card


@receiver(signals.post_save, sender=Card)
def create_card_placement_for_new_card(instance, created, **kwargs):
    if created:
        CardPlacement.objects.create(
            card=instance,
            user=instance.category.owner,
        )
