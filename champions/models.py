from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings
from accounts.models import Player



def validate_less_than_7(value):
        if value > 7:
            raise ValidationError(
                ('%(value)s is more than 7'),
                params={'value': value},
            )


class ChampionMastery(models.Model):
    points = models.IntegerField()
    title = models.CharField(max_length=50)
    level = models.IntegerField(validators=[validate_less_than_7])
    profile = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE, related_name='masteries', null=True)
    champion = models.ForeignKey('Champion', on_delete=models.CASCADE, related_name='masteries', null=True)
    # @admin.display(description='')
    # def highest_mastery(self):
    #     return Profile.objects.aggregate(highest_mastery=Max('highest_champion_mastery__points'))
    class Meta:
        verbose_name_plural = "Masteries"
        
    def __str__(self) -> str:
        return f'{self.points}'
    

class ChampionMasteryImage(models.Model):
    mastery = models.ForeignKey(ChampionMastery, related_name='images', on_delete=models.CASCADE)
    icon = models.ImageField(null=True, blank=True)

    

class EternalGroup(models.Model):
    name = models.CharField(max_length=50)
    is_unlocked =  models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return f'{self.name}'

class EternalGroupImage(models.Model):
    group = models.ForeignKey(EternalGroup, related_name='images', on_delete=models.CASCADE, null=True)
    icon = models.ImageField(null=True, blank=True)
    
class Eternal(models.Model):
    score = models.IntegerField()
    name = models.CharField(max_length=50)
    group = models.ForeignKey(EternalGroup, on_delete=models.CASCADE, null=True)
    champion = models.ForeignKey('Champion', on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return f'{self.name}'


class EternalImage(models.Model):
    eternal = models.ForeignKey(Eternal, related_name='images', on_delete=models.CASCADE)
    icon = models.ImageField(null=True, blank=True)


class ChampionAbility(models.Model):
    key = models.IntegerField()
    name = models.CharField(max_length=60)
    is_ultimate =  models.BooleanField(default=False)
    description = models.TextField()
    video_showcase = models.FileField(null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.name}'

    class Meta:
        verbose_name_plural = "Abillities"

class ChampionAbilityImage(models.Model):
    champion_ability = models.ForeignKey(ChampionAbility, related_name='images', on_delete=models.CASCADE)
    icon = models.ImageField(null=True, blank=True)


class ChampionSkin(models.Model):
    class SkinRarity(models.IntegerChoices):
        RARE = 0
        EPIC = 1
        LEGENDARY = 2
        ULTIMATE = 3
    name = models.CharField(max_length=50)
    skin_rarity = models.IntegerField(choices=SkinRarity.choices, default=SkinRarity.RARE)

    class Meta:
        verbose_name_plural = "Skins"
    
    def __str__(self) -> str:
        return f'{self.name}'

class ChampionSkinImage(models.Model):
    champion_skin = models.ForeignKey(ChampionSkin, related_name='images', on_delete=models.CASCADE)
    look = models.ImageField(null=True, blank=True)
    border = models.ImageField(null=True, blank=True)



class Champion(models.Model):
    class Category(models.IntegerChoices):
        DAMAGE = 0
        TOUGHNESS = 1
        CROWD_CONTROL = 2
        MOBILITY = 3
        UTILITY = 4
    
    class DamageType(models.IntegerChoices):
        ATTACK_DAMAGE = 0
        ABILITY_POWER = 1
        

    class PriceRP(models.IntegerChoices):
        _275 = 275    
        _975 = 975
        _1350 = 1350
        _1820 = 1820
        _3250 = 3250

    class PriceBE(models.IntegerChoices):
        _450 = 450   
        _1350 = 1350
        _3150 = 3150
        _4800 = 4800
        _6300 = 6300
        _7800 = 7800
        
    class DifficultyOptions(models.IntegerChoices):
        EASY = 0   
        NORMAL = 1
        HARD = 2
        VERYDIFFICULT = 3

    
    

    name = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    price_rp = models.IntegerField(choices=PriceRP.choices)
    price_be = models.IntegerField(choices=PriceBE.choices)
    type = models.ImageField(null=True, blank=True)
    category = models.IntegerField(choices=Category.choices, null=True, blank=True)
    damage_type = models.IntegerField(choices=DamageType.choices, null=True, blank=True)
    style = models.ImageField(null=True, blank=True)
    difficulty = models.IntegerField(choices=DifficultyOptions.choices, null=True, blank=True)
    description = models.TextField()
    is_freetoplay = models.BooleanField(default=False)
    disabled = models.BooleanField(default=False)
    release_date = models.DateTimeField(auto_now_add=True)
    abilities = models.ForeignKey(ChampionAbility, on_delete=models.CASCADE, null=True)
    skins = models.ForeignKey(ChampionSkin, on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return f'{self.name}'
    
    
class ChampionImage(models.Model):
    champion = models.ForeignKey(Champion, related_name='images', on_delete=models.CASCADE)
    type = models.ImageField(null=True, blank=True)
    style = models.ImageField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    

  
class SkinOwnerShip(models.Model):
    player = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='skins')
    skin = models.ForeignKey(ChampionSkin, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.IntegerField()
    payment_currency = models.IntegerField(choices=Player.PaymentCurrency.choices, null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.player} owns {self.skin}'

class ChampionOwnerShip(models.Model):
    player = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='champions')
    champion = models.ForeignKey(Champion, on_delete=models.CASCADE,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.IntegerField()
    payment_currency = models.IntegerField(choices=Player.PaymentCurrency.choices)
    
    def __str__(self) -> str:
        return f'{self.player} owns {self.champion}'

