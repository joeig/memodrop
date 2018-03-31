from django.db import models
from django.urls import reverse
from django.utils import timezone


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
    area = models.IntegerField(default=1, choices=AREA_CHOICES, verbose_name='Area')
    category = models.ForeignKey('categories.Category', on_delete=models.CASCADE, related_name='cards')
    last_interaction = models.DateTimeField(auto_now_add=True, blank=True, editable=False)
    objects = models.Manager()
    user_objects = CardUserManager()

    class Meta:
        ordering = ['area']

    def __str__(self):
        return 'Card #{}'.format(self.pk)

    def get_absolute_url(self):
        return reverse('card-detail', kwargs={'pk': self.pk})

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
