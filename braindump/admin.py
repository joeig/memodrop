from django.contrib import admin

from braindump.models import CardPlacement


class CardPlacementAdmin(admin.ModelAdmin):
    list_display = ('card', 'user', 'area', 'postpone_until', 'last_interaction')
    list_filter = ('user',)


admin.site.register(CardPlacement, CardPlacementAdmin)
