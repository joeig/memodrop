from django.contrib import admin

from authentication.models import UserGUISettings


class UserGUISettingsAdmin(admin.ModelAdmin):
    list_display = ('user', 'enable_markdown_editor')
    list_filter = ('user', 'enable_markdown_editor')
    search_fields = ('user', 'enable_markdown_editor')


admin.site.register(UserGUISettings, UserGUISettingsAdmin)
