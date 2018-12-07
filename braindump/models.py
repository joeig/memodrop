from django.conf import settings
from django.db import models
from django.utils import timezone


class CardPlacementUserManager(models.Manager):
    def all(self, user):
        """Returns all card placements belonging to the user
        """
        return self.filter(user=user).all()

    def get(self, user, *args, **kwargs):
        """Returns a card placement belonging to the user
        """
        return self.filter(user=user).get(*args, **kwargs)


class CardPlacementCardManager(models.Manager):
    def all(self, card):
        """Returns all card placements belonging to a card
        """
        return self.filter(card=card).all()

    def get(self, card, *args, **kwargs):
        """Returns a card placement belonging to a card
        """
        return self.filter(card=card).get(*args, **kwargs)


class CardPlacementCardUserManager(models.Manager):
    def get(self, card, user, *args, **kwargs):
        """Returns a card placement belonging to a card and the user
        """
        return self.filter(card=card, user=user).get(*args, **kwargs)


class CardPlacement(models.Model):
    AREA_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
    )
    area = models.IntegerField(default=1, choices=AREA_CHOICES, verbose_name='Area')
    card = models.ForeignKey('cards.Card', on_delete=models.CASCADE, related_name='card_placements')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    last_interaction = models.DateTimeField(auto_now_add=True, blank=True, editable=False)
    postpone_until = models.DateTimeField(default=timezone.now, blank=True)
    objects = models.Manager()
    user_objects = CardPlacementUserManager()
    card_objects = CardPlacementCardManager()
    card_user_objects = CardPlacementCardUserManager()

    class Meta:
        unique_together = (('card', 'user'),)
        ordering = ['area']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['card']),
        ]

    def move_forward(self):
        """Increase the area
        """
        if self.area < 6:
            self.area += 1
            self.save()

    def move_backward(self):
        """Decrease the area
        """
        if self.area > 1:
            self.area -= 1
            self.save()

    def reset(self):
        """Set card to area 1
        """
        self.area = 1
        self.save()

    def set_last_interaction(self, last_interaction=False):
        """Set date and time of last interaction
        """
        if not last_interaction:
            last_interaction = timezone.now()
        self.last_interaction = last_interaction
        self.save()

    def postponed(self):
        """Return true if card has been postponed
        """
        if self.postpone_until > timezone.now():
            return True
        else:
            return False

    def expedite(self):
        """Reset postpone marker
        """
        self.postpone_until = timezone.now()
        self.save()
