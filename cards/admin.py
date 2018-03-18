from django.contrib import admin

from cards.models import Card


class CardAdmin(admin.ModelAdmin):
    list_display = ('question', 'area', 'category')


admin.site.register(Card, CardAdmin)
