from django.contrib import admin

from categories.models import Category, ShareContract


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'mode', 'owner')
    list_filter = ('mode', 'owner')
    search_fields = ('name', 'description')
    readonly_fields = ('owner',)


class ShareContractAdmin(admin.ModelAdmin):
    list_display = ('category', 'user', 'accepted')
    list_filter = list_display
    readonly_fields = list_display


admin.site.register(Category, CategoryAdmin)
admin.site.register(ShareContract, ShareContractAdmin)
