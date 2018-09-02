from django.db.models import signals
from django.dispatch import receiver
from django_q.tasks import async_task, async_chain

from braindump.models import CardPlacement
from cards.models import Card
from categories.models import ShareContract
from categories.signals import share_contract_accepted, share_contract_revoked


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
def share_contract_accepted(share_contract, **kwargs):
    """Signal handler for share contracts that have been accepted
    """
    async_task('braindump.tasks.create_card_placements_for_shared_category', share_contract)


@receiver(share_contract_revoked, sender=ShareContract)
def share_contract_revoked(share_contract, **kwargs):
    """Signal handler for shared contracts that have been deleted
    """
    # Do this only if the share contract was accepted:
    if share_contract.accepted:
        async_chain([
            ('braindump.tasks.create_independent_category', (share_contract,)),
            ('braindump.tasks.delete_revoked_share_contract', (share_contract,)),
         ])
