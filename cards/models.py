from django.db import models
from django.urls import reverse


class CardOwnerManager(models.Manager):
    def all(self, user):
        """Returns all cards belonging to the category's owner
        """
        return self.filter(category__owner=user).all()

    def get(self, user, *args, **kwargs):
        """Returns a card belonging to the category's owner
        """
        return self.filter(category__owner=user).get(*args, **kwargs)


class CardSharedManager(models.Manager):
    def all(self, user):
        """Returns all cards belonging to the category's owner
        """
        return self.filter(category__share_contracts__user=user, category__share_contracts__accepted=True).all()

    def get(self, user, *args, **kwargs):
        """Returns a card belonging to the category's owner
        """
        return self.filter(category__share_contracts__user=user, category__share_contracts__accepted=True).get(*args,
                                                                                                               **kwargs)


class Card(models.Model):
    AREA_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
    )
    question = models.TextField(verbose_name='Question')
    answer = models.TextField(verbose_name='Answer')
    hint = models.TextField(blank=True, verbose_name='Hint')
    category = models.ForeignKey('categories.Category', on_delete=models.CASCADE, related_name='cards')
    objects = models.Manager()
    owned_objects = CardOwnerManager()
    shared_objects = CardSharedManager()

    def __str__(self):
        return 'Card #{}'.format(self.pk)

    def get_absolute_url(self):
        return reverse('card-detail', kwargs={'pk': self.pk})

    def is_shared_with(self):
        """Returns a list of users this card is shared with
        """
        return [s.user for s in self.category.share_contracts.filter(accepted=True)]
