from django.db import models
from django.conf import settings
import strawberry


class Loot(models.Model):
    @strawberry.enum
    class Category(models.IntegerChoices):
        WARD_SKIN = 0
        SKIN = 1
        CHAMPION = 2
        MATERIAL = 3
        TACTICAL = 4
        ETERNAL = 5
        EMOTE = 6
        ICON = 7

    @strawberry.enum
    class Currency(models.IntegerChoices):
        BLUE_ESSENCE = 0
        ORANGE_ESSENCE = 1
        EVENT_COINS = 2

    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.IntegerField()
    category = models.IntegerField(choices=Category.choices)
    currency = models.IntegerField(choices=Currency.choices)

    class Meta:
        verbose_name_plural = "Loot"

    def __str__(self) -> str:
        return f"{self.name}"


class LootOwnerShip(models.Model):
    player = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="loots",
    )
    loot = models.ForeignKey("Loot", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.player} owns {self.loot}"


class LootImage(models.Model):
    loot = models.ForeignKey(
        Loot, related_name="images", on_delete=models.CASCADE, null=True
    )
    image = models.ImageField(default="image 2.jpg")
