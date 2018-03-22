from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone


class CategoryUserManager(models.Manager):
    def all(self, owner):
        """Returns all categories belonging to the authorized user
        """
        return self.filter(owner=owner).all()

    def get(self, owner, *args, **kwargs):
        """Returns a category belonging to the authorized user
        """
        return self.filter(owner=owner).get(*args, **kwargs)


class Category(models.Model):
    MODE_CHOICES = (
        (1, 'Strict'),
        (2, 'Defensive'),
    )
    name = models.CharField(max_length=128)
    description = models.TextField(verbose_name='Description (Markdown)')
    mode = models.IntegerField(default=1, choices=MODE_CHOICES)
    last_interaction = models.DateTimeField(auto_now_add=True, blank=True, editable=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    objects = models.Manager()
    user_objects = CategoryUserManager()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """Get the absolute URL to a single card
        """
        return reverse('category-detail', kwargs={'pk': self.pk})

    def get_cards_for_area(self, area):
        """Get all cards of a specific area
        """
        return self.cards.filter(area=area)

    def set_last_interaction(self, last_interaction=timezone.now()):
        """Set date and time of last interaction
        """
        self.last_interaction = last_interaction
        self.save()
