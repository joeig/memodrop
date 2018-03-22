from django.contrib import admin

from cards.models import Card


class CardAdmin(admin.ModelAdmin):
    list_display = ('question', 'area', 'category', 'last_interaction')
    list_filter = ('area', 'category')
    search_fields = ('question', 'hint', 'answer')


admin.site.register(Card, CardAdmin)
