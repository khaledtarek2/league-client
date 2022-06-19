from django.contrib import admin
from loot.models import Loot, LootImage, LootOwnerShip

class LootOwnerShipInline(admin.StackedInline):
    model = LootOwnerShip
    extra = 2
    
class LootImageInline(admin.TabularInline):
    model = LootImage
    extra = 3
    

class LootAdmin(admin.ModelAdmin):
    fields = ['name', 'description','price',
            'type', 'currency']
    list_display = ('name', 'description','price',
            'type', 'currency')
    list_filter = ['type', 'currency']
    search_fields = ['name', 'price']
    inlines = [LootOwnerShipInline, LootImageInline] 


class LootOwnerShipAdmin(admin.ModelAdmin):
    fields = ['player', 'loot','paid',
            'purchasing_currency']
    list_display = ('player', 'loot','created_at','paid',)
    list_filter = ['paid', 'created_at']
    search_fields = ['player__username']



admin.site.register(Loot, LootAdmin)
admin.site.register(LootOwnerShip, LootOwnerShipAdmin)

