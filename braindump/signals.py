from django.db.models import signals
from django.dispatch import receiver

from braindump.models import CardPlacement
from cards.models import Card
from categories.models import ShareContract, Category
from categories.signals import share_contract_accepted


@receiver(signals.post_save, sender=Card)
def create_card_placement_for_new_card(instance, created, **kwargs):
    """Creates a card placement for a recently created card
    """
    if created:
        CardPlacement.objects.create(
            card=instance,
            user=instance.category.owner,
        )

        for share_contract in instance.category.share_contracts.filter(accepted=True):
            CardPlacement.objects.create(
                card=instance,
                user=share_contract.user,
            )


@receiver(share_contract_accepted, sender=ShareContract)
def create_card_placements_for_shared_category(share_contract, **kwargs):
    """Creates card placements for a recently accepted share contract
    """
    for card in share_contract.category.cards.all():
        CardPlacement.objects.create(
            card=card,
            user=share_contract.user,
        )


@receiver(signals.pre_delete, sender=ShareContract)
def create_independent_category(instance, **kwargs):
    """Duplicates an existing category with its cards and moves all necessary card placements
    """
    # Do this only if the share contract was accepted:
    if instance.accepted:
        # Duplicate category:
        new_category = Category.objects.get(pk=instance.category.pk)
        new_category.pk = None
        new_category.owner = instance.user
        new_category.save()

        for card in instance.category.cards.all():
            # Duplicate card:
            new_card = Card.objects.get(pk=card.pk)
            new_card.pk = None
            new_card.category = new_category
            new_card.save()  # this will be creating a new card placement automatically

            # Remove the auto-generated card placement:
            CardPlacement.card_user_objects.get(card=new_card, user=instance.user).delete()

            # Move existing card placement to the new card:
            card_placement = CardPlacement.card_user_objects.get(card=card, user=instance.user)
            card_placement.card = new_card
            card_placement.save()
