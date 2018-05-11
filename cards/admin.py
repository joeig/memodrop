from django.contrib import admin

from cards.models import Card


class CardAdmin(admin.ModelAdmin):
    list_display = ('question', 'category')
    list_filter = ('category',)
    search_fields = ('question', 'hint', 'answer')

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('category',)
        return self.readonly_fields


admin.site.register(Card, CardAdmin)
