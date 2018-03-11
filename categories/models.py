from django.db import models
from django.urls import reverse
from django.utils import timezone


class Category(models.Model):
    MODE_CHOICES = (
        (1, 'Strict'),
        (2, 'Defensive'),
    )
    name = models.CharField(max_length=128)
    description = models.TextField(verbose_name='Description (Markdown)')
    mode = models.IntegerField(default=1, choices=MODE_CHOICES)
    last_interaction = models.DateTimeField(auto_now_add=True, blank=True, editable=False)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category-detail', kwargs={'pk': self.pk})

    def get_cards_for_area(self, area):
        return self.cards.filter(area=area)

    def set_last_interaction(self, last_interaction=timezone.now()):
        self.last_interaction = last_interaction
        self.save()
