from django.contrib import admin

from store.models import Item



class ItemAdmin(admin.ModelAdmin):
    fields = ['name', 'stats', 'passive','active', 'type']
    list_display = ('name', 'stats', 'passive','active', 'type')
    list_filter = ['type']


    
admin.site.register(Item, ItemAdmin)