from django.db import models

class Item(models.Model):
    class Type(models.IntegerChoices):
            fighter = 0
            marksman = 1
            assassin = 2
            mage = 3
            tank = 4
            support = 5
    name = models.CharField(max_length=60, null=True, blank=True)    
    stats = models.JSONField(null=True, blank=True)
    passive = models.TextField(null=True, blank=True)
    active = models.TextField(null=True, blank=True)
    type = models.IntegerField(choices=Type.choices, null=True, blank=True)
    
    def __str__(self) -> str:
        return f'{self.name}'

