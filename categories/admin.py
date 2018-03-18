from django.contrib import admin

from categories.models import Category


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'mode', 'owner')


admin.site.register(Category, CategoryAdmin)
