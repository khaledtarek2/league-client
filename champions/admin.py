from django.contrib import admin
from champions.models import ( Champion, ChampionImage, ChampionSkin, ChampionAbility, EternalGroupImage, Eternal,
                              EternalGroup, ChampionMastery, ChampionMasteryImage, ChampionSkinImage,
                              ChampionAbilityImage, EternalImage,SkinOwnerShip, ChampionOwnerShip)


class ChampionMasteryImageInline(admin.TabularInline):
    model = ChampionMasteryImage
    extra = 3
    
    
class ChampionImageInline(admin.TabularInline):
    model = ChampionImage
    extra = 3
    
    
class ChampionSkinImageInline(admin.TabularInline):
    model = ChampionSkinImage
    extra = 3
    

class ChampionAbilityImageInline(admin.TabularInline):
    model = ChampionAbilityImage
    extra = 3


 
class EternalImageInline(admin.TabularInline):
    model = EternalImage
    extra = 3    
 

class EternalGroupImageInline(admin.TabularInline):
    model = EternalGroupImage
    extra = 3

  
class ChampionAdmin(admin.ModelAdmin):
    fieldsets = (
        ('ChampionInfo', {
            'fields': ('name', 'title', 'price_rp', 'price_be', 'type')
                           }),
        
        ('ChampionType', {
            'fields': ('category', 'damage_type')
            }),
        
        ('Personalized', {
            'fields': ('style', 'difficulty', 'description', 'is_freetoplay', 'abilities',
                       'skins', 'disabled')
            }),

    )
    list_display = ('name', 'title', 'type', 'price_be', 'is_freetoplay', 'disabled')
    list_filter = ['is_freetoplay', 'release_date', 'difficulty', 'category', 'damage_type', 'disabled']
    search_fields = ['name', 'title', 'price_rp', 'price_be', 'type', 'category']
    ordering = ['release_date']
    inlines = [ChampionImageInline]


class ChampionSkinAdmin(admin.ModelAdmin):
    fields = ['name', 'skin_rarity']
    list_display = ('name', 'skin_rarity')
    search_fields = ['name']
    list_filter = ['skin_rarity']
    inlines = [ChampionSkinImageInline]


class ChampionAbilityAdmin(admin.ModelAdmin):
    fields = ['key', 'name', 'is_ultimate', 'description', 'video_showcase']
    list_display = ('key', 'name')
    search_fields = ['key', 'name']
    list_filter = ['key', 'is_ultimate']
    inlines = [ChampionAbilityImageInline]

    
class EternalGroupAdmin(admin.ModelAdmin):
    fields = ['name', 'is_unlocked']
    list_display = ('name', 'is_unlocked')
    search_fields = ['name']
    list_filter = ['is_unlocked']
    inlines = [EternalGroupImageInline]
    
class EternalAdmin(admin.ModelAdmin):
    fields = ['name', 'score', 'group', 'champion']
    list_display = ('name', 'score', 'group', 'champion')
    search_fields = ['name', 'score', 'group__name', 'champion__name']
    list_filter = ['group', 'champion']
    inlines = [EternalImageInline]
 
       
    
class ChampionMasteryAdmin(admin.ModelAdmin):
    fields = ['points', 'title', 'level', 'profile', 'champion']
    list_display = ('points', 'title', 'level', 'profile', 'champion')
    search_fields = ['points', 'level', 'title']
    inlines = [ ChampionMasteryImageInline]
    
    

class SkinOwnerShipAdmin(admin.ModelAdmin):
    fields = ['player', 'skin', 'paid', 'payment_currency']
    list_display = ('player', 'skin', 'created_at', 'paid', 'payment_currency')
    search_fields = ['player__username', 'skin__name', 'paid']
    list_filter = ['created_at', 'payment_currency']


class ChampionOwnerShipAdmin(admin.ModelAdmin):
    fields = ['player', 'champion', 'paid', 'payment_currency']
    list_display = ('player', 'champion', 'created_at', 'paid', 'payment_currency')
    search_fields = ['player__username', 'champion__name', 'paid']
    list_filter = ['created_at', 'payment_currency']
    
    
admin.site.register(Champion, ChampionAdmin)
admin.site.register(ChampionSkin, ChampionSkinAdmin)
admin.site.register(ChampionAbility, ChampionAbilityAdmin)
admin.site.register(Eternal, EternalAdmin)
admin.site.register(EternalGroup, EternalGroupAdmin)
admin.site.register(ChampionMastery, ChampionMasteryAdmin)
admin.site.register(SkinOwnerShip, SkinOwnerShipAdmin)
admin.site.register(ChampionOwnerShip, ChampionOwnerShipAdmin)

    
