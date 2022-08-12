from django.db import models
import strawberry


class Item(models.Model):
    @strawberry.enum
    class Category(models.IntegerChoices):
        fighter = 0
        marksman = 1
        assassin = 2
        mage = 3
        tank = 4
        support = 5

    name = models.CharField(max_length=60)
    stats = models.JSONField(default=dict)
    passive = models.TextField(default="passive")
    active = models.TextField(default="active")
    category = models.IntegerField(choices=Category.choices, default=Category.fighter)

    def __str__(self) -> str:
        return f"{self.name}"
