import logging

from braindump.models import CardPlacement
from cards.models import Card
from categories.models import Category


logger = logging.getLogger(__name__)


def create_card_placements_for_shared_category(share_contract):
    """Creates card placements for a recently accepted share contract
    """
    for card in share_contract.category.cards.all():
        logger.info('Creating card placement for share contract #{}, card #{} and user #{}'.format(
            share_contract.pk, card.pk, share_contract.user.pk
        ))
        CardPlacement.objects.create(
            card=card,
            user=share_contract.user,
        )


def create_independent_category(share_contract):
    """Duplicates an existing category with its cards and moves all necessary card placements
    """
    # Duplicate category:
    logger.info('Duplicating category #{}'.format(share_contract.category.pk))
    new_category = Category.objects.get(pk=share_contract.category.pk)
    new_category.pk = None
    new_category.owner = share_contract.user
    new_category.save()
    logger.debug('New category is #{}'.format(share_contract.category.pk, new_category.pk))

    for card in share_contract.category.cards.all():
        # Duplicate card:
        logger.info('Duplicating card #{}'.format(card.pk))
        new_card = Card.objects.get(pk=card.pk)
        new_card.pk = None
        new_card.category = new_category
        new_card.save()  # this will be creating a new card placement automatically
        logger.debug('New card is #{}'.format(card.pk, new_card.pk))

        # Remove the auto-generated card placement:
        automatic_card_placement = CardPlacement.card_user_objects.get(card=new_card, user=share_contract.user)
        logger.debug('Removing auto-generated card placement #{}'.format(automatic_card_placement.pk))
        automatic_card_placement.delete()

        # Move existing card placement to the new card:
        card_placement = CardPlacement.card_user_objects.get(card=card, user=share_contract.user)
        logger.debug('Moving existing card placement #{} to recently created card #{}'.format(
            card_placement.pk, new_card.pk
        ))
        card_placement.card = new_card
        card_placement.save()


def delete_revoked_share_contract(share_contract):
    """Deletes a revoked share contract
    """
    if share_contract.accepted and share_contract.revoked:
        logger.info('Deleting revoked share contract #{}'.format(share_contract.pk))
        share_contract.delete()
    else:
        logger.warning('Refuse to delete revoked share contract #{}, because it has not been accepted yet'.format(
            share_contract.pk
        ))
