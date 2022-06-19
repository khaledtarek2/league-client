from django.db import models
from django.conf import settings


class Loot(models.Model):
    class LootType(models.IntegerChoices):
        WARD_SKIN = 0
        SKIN = 1
        CHAMPION = 2
        MATERIAL = 3
        TACTICAL = 4
        ETERNAL = 5
        EMOTE = 6
        ICON = 7
        
        
    class LootCurrency(models.IntegerChoices):
        BLUE_ESSENCE = 0
        ORANGE_ESSENCE = 1
        EVENT_COINS = 2 
        
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.IntegerField()
    type = models.IntegerField(choices=LootType.choices)
    currency = models.IntegerField(choices=LootCurrency.choices)
    
    class Meta:
        verbose_name_plural = "Loot"


    def __str__(self) -> str:
        return f'{self.name}'  

class LootOwnerShip(models.Model):
    player = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name='loots')
    loot = models.ForeignKey('Loot', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.IntegerField()
     
    def __str__(self) -> str:
        return f'{self.player} owns {self.loot}'
    
    

class LootImage(models.Model):
    loot = models.ForeignKey(Loot, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField()