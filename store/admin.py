from django.contrib import admin

from store.models import Item


class ItemAdmin(admin.ModelAdmin):
    fields = ["name", "stats", "passive", "active", "category"]
    list_display = ("name", "stats", "passive", "active", "category")
    list_filter = ["category"]


admin.site.register(Item, ItemAdmin)
