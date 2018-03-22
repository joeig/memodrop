from django.contrib import admin

from categories.models import Category


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'mode', 'owner', 'last_interaction')
    list_filter = ('mode', 'owner')
    search_fields = ('name', 'description')


admin.site.register(Category, CategoryAdmin)
