from django.db import models
from django.urls import reverse


class Category(models.Model):
    MODE_CHOICES = (
        (1, 'Strict'),
        (2, 'Defensive'),
    )
    name = models.CharField(max_length=128)
    description = models.TextField(verbose_name='Description (Markdown)')
    mode = models.IntegerField(default=1, choices=MODE_CHOICES)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category-detail', kwargs={'pk': self.pk})

    def get_cards_for_area(self, area):
        return self.cards.filter(area=area)
