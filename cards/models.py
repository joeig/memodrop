from django.db import models
from django.urls import reverse


class CardUserManager(models.Manager):
    def all(self, user):
        """Returns all cards belonging to the authorized user
        """
        return self.filter(category__owner=user).all()

    def get(self, user, *args, **kwargs):
        """Returns a card belonging to the authorized user
        """
        return self.filter(category__owner=user).get(*args, **kwargs)


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
    user_objects = CardUserManager()

    def __str__(self):
        return 'Card #{}'.format(self.pk)

    def get_absolute_url(self):
        return reverse('card-detail', kwargs={'pk': self.pk})
