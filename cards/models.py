from django.db import models
from django.db.models import F
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
    _area = models.IntegerField(default=1, choices=AREA_CHOICES, verbose_name='Area')
    category = models.ForeignKey('categories.Category', on_delete=models.PROTECT)

    class Meta:
        ordering = ['_area']

    def __str__(self):
        return 'Card #{}'.format(self.pk)

    @property
    def area(self):
        """Getter for self.area
        """
        return self._area

    @area.setter
    def area(self, value):
        """Setter for self.area
        """
        self._area = value

    def get_absolute_url(self):
        return reverse('card-detail', kwargs={'pk': self.pk})

    def move_forward(self):
        """Increase the area
        """
        self.area = F('_area') + 1
        self.save()

    def move_backward(self):
        """Decrease the area
        """
        self.area = F('_area') - 1
        self.save()

    def reset(self):
        """Set card to area 1
        """
        self.area = 1
        self.save()
