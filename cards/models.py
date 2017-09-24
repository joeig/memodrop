from django.db import models
from django.urls import reverse


class Card(models.Model):
    AREA_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
    )
    question = models.TextField()
    answer = models.TextField()
    hint = models.TextField(blank=True)
    area = models.IntegerField(default=1, choices=AREA_CHOICES)
    category = models.ForeignKey('categories.Category', on_delete=models.PROTECT)

    class Meta:
        ordering = ['area']

    def __str__(self):
        return 'Card #{}'.format(self.pk)

    def get_absolute_url(self):
        return reverse('card-detail', kwargs={'pk': self.pk})

    def move_forward(self):
        """Increase the area
        """
        if self.area != 6:
            self.area = self.area + 1
            self.save()

    def move_backward(self):
        """Decrease the area
        """
        if self.area != 1:
            self.area = self.area - 1
            self.save()

    def reset(self):
        """Set card to area 1
        """
        self.area = 1
        self.save()
