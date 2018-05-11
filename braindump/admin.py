from django.contrib import admin

from braindump.models import CardPlacement


class CardPlacementAdmin(admin.ModelAdmin):
    list_display = ('card', 'user', 'area', 'postpone_until', 'last_interaction')
    list_filter = ('user',)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('card', 'user')
        return self.readonly_fields

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(CardPlacement, CardPlacementAdmin)
