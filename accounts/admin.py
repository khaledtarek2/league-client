from django.contrib import admin
from django.contrib.auth import get_user_model
from champions.models import Champion, ChampionMastery
from .models import Rank, PlayerSeasonGrade, Profile, PlayerImage, Message, RankImage, ProfileImage
from django.utils.html import format_html, format_html_join
from django.utils.safestring import mark_safe



class PlayerImageInline(admin.TabularInline):
    model = PlayerImage
    extra = 3
    

class RankImageInline(admin.TabularInline):
    model = RankImage
    extra = 3
    

class ProfileImageInline(admin.TabularInline):
    model = ProfileImage
    extra = 3
    
class PlayerAdmin(admin.ModelAdmin):
    fieldsets = (
        ('PlayerDetails', {
            'fields': ('username', 'password', 'email', 'is_online')
                           }),
        
        ('PersonalizedData', {
            'fields': ('level', 'server', 'profile', 'friends')
            }),
        
        # ('Ownage', {
        #     'fields': ('owned_loot')
        #     }),

    )
    list_display = ('username', 'profile', 'email', 'is_online', 'date_joined')
    list_filter = ['is_online', 'date_joined', 'server']
    inlines = [ PlayerImageInline]
    search_fields = ['username', 'level']
    ordering = ['date_joined']
    
    
    
class RankAdmin(admin.ModelAdmin):
    fields = ['type', 'rank']
    list_display = ('type', 'rank')
    list_filter = ['type', 'rank']
    inlines = [RankImageInline]




class PlayerSeasonGradeAdmin(admin.ModelAdmin):
    fields = ['player', 'champion', 'grade']
    list_display = ('player', 'champion', 'grade', 'obtained_at')
    search_fields = ['player__username', 'champion__name', 'obtained_at']
    list_filter = ['grade']
    

class ProfileAdmin(admin.ModelAdmin):
    fields = ['rank', 'honor_level', 'top_three']
    readonly_fields = ['top_three']
    list_display = ('rank', 'honor_level')
    search_fields = ['rank__rank', 'rank__rank_type']
    list_filter = ['honor_level']
    inlines = [ProfileImageInline]

 
    @admin.display()
    def top_three(self, profile):
        t3 =  profile.mastries.all().order_by('-points')[:3]
        html = """ 

<ul> {% for champion_mastry in mastries %}

<li> {{ champion_mastry.champion.name }} {{ champion.champion_mastry.points }} </li>
{% endfor %}
</ul>"""
        weired_html = """

<ul> {}

<li> {} {} </li>
{}
</ul>"""
        html_ = "<li>{} : {}</li>"
                   
            # return format_html("""<ul> {% for champion_mastry in mastries %}

            # <li> {{ champion_mastry.champion.name }} {{ champion.champion_mastry.points }} </li>
            #     {% endfor %}
            # </ul>""", mark_safe(html))

        for champion_m in ChampionMastery.objects.all():
            pass
        # for profile in Profile.objects.all():
        #     pass
        for champion in Champion.objects.all():
            pass
        # msg = format_html_join('\n', html,
        #     ((*champion_mastry.champion, *profile.champion_mastry) for champion_mastry in profile.mastries.all())
        # )
        return format_html(
                "<ul><li>{}</li></ul>",
                ((champion_m.champion.name, profile.mastries.get(pk=champion_m.champion.pk)),
                 (champion_m.champion.name, profile.mastries.get(pk=champion_m.champion.pk)),
                 (champion_m.champion.name, profile.mastries.get(pk=champion_m.champion.pk))
                ))
    top_three.allow_tags = True
    # champion_mastry.champion.all,


admin.site.register(get_user_model(), PlayerAdmin)
admin.site.register(Rank, RankAdmin)
admin.site.register(PlayerSeasonGrade, PlayerSeasonGradeAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Message)
 # return list(t3.values_list('points'))
