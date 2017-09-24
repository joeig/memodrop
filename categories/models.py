from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category-detail', kwargs={'pk': self.pk})

    def get_cards_for_area(self, area):
        return self.card_set.filter(area=area)
