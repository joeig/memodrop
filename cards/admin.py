from django.contrib import admin

from cards.models import Card


class CardAdmin(admin.ModelAdmin):
    list_display = ('question', 'category')
    list_filter = ('category',)
    search_fields = ('question', 'hint', 'answer')


admin.site.register(Card, CardAdmin)
