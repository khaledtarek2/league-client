from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings
import strawberry
from accounts.models import Player


def validate_less_than_7(value):
    if value > 7:
        raise ValidationError(
            ("%(value)s is more than 7"),
            params={"value": value},
        )


class ChampionMastery(models.Model):
    points = models.IntegerField()
    title = models.CharField(max_length=50)
    level = models.IntegerField(default=3, validators=[validate_less_than_7])
    player = models.ForeignKey(
        "accounts.Player",
        on_delete=models.CASCADE,
        related_name="masteries",
        null=True,
    )
    champion = models.ForeignKey(
        "Champion", on_delete=models.CASCADE, related_name="masteries", null=True
    )
    # @admin.display(description='')
    # def highest_mastery(self):
    #     return Profile.objects.aggregate(highest_mastery=Max('highest_champion_mastery__points'))
    class Meta:
        verbose_name_plural = "Masteries"

    def __str__(self) -> str:
        return f"{self.points}"


class ChampionMasteryImage(models.Model):
    mastery = models.ForeignKey(
        ChampionMastery, related_name="images", on_delete=models.CASCADE
    )
    icon = models.ImageField(default="image 2.jpg")


class EternalGroup(models.Model):
    name = models.CharField(max_length=50, unique=True)
    is_unlocked = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.name}"


class EternalGroupImage(models.Model):
    group = models.ForeignKey(
        EternalGroup, related_name="images", on_delete=models.CASCADE
    )
    icon = models.ImageField(default="image 2.jpg")


class Eternal(models.Model):
    score = models.IntegerField()
    name = models.CharField(max_length=50, unique=True)
    group = models.ForeignKey(EternalGroup, on_delete=models.CASCADE)
    champion = models.ForeignKey("Champion", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.name}"


class EternalImage(models.Model):
    eternal = models.ForeignKey(
        Eternal, related_name="images", on_delete=models.CASCADE
    )
    icon = models.ImageField(default="image 2.jpg")


class ChampionAbility(models.Model):
    key = models.IntegerField()
    name = models.CharField(max_length=60, unique=True)
    is_ultimate = models.BooleanField(default=False)
    description = models.TextField()

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        verbose_name_plural = "Abillities"


class ChampionAbilityImage(models.Model):
    champion_ability = models.ForeignKey(
        ChampionAbility, related_name="images", on_delete=models.CASCADE
    )
    icon = models.ImageField(default="image 2.jpg")


class ChampionSkin(models.Model):
    @strawberry.enum
    class SkinRarity(models.IntegerChoices):
        RARE = 0
        EPIC = 1
        LEGENDARY = 2
        ULTIMATE = 3

    name = models.CharField(max_length=50, unique=True)
    skin_rarity = models.IntegerField(
        choices=SkinRarity.choices, default=SkinRarity.RARE
    )

    class Meta:
        verbose_name_plural = "Skins"

    def __str__(self) -> str:
        return f"{self.name}"


class ChampionSkinImage(models.Model):
    champion_skin = models.ForeignKey(
        ChampionSkin, related_name="images", on_delete=models.CASCADE
    )
    look = models.ImageField(default="image 2.jpg")
    border = models.ImageField(default="image 2.jpg")


class Champion(models.Model):
    @strawberry.enum
    class Category(models.IntegerChoices):
        DAMAGE = 0
        TOUGHNESS = 1
        CROWD_CONTROL = 2
        MOBILITY = 3
        UTILITY = 4

    @strawberry.enum
    class DamageType(models.IntegerChoices):
        ATTACK_DAMAGE = 0
        ABILITY_POWER = 1

    @strawberry.enum
    class PriceRP(models.IntegerChoices):
        _275 = 275
        _975 = 975
        _1350 = 1350
        _1820 = 1820
        _3250 = 3250

    @strawberry.enum
    class PriceBE(models.IntegerChoices):
        _450 = 450
        _1350 = 1350
        _3150 = 3150
        _4800 = 4800
        _6300 = 6300
        _7800 = 7800

    @strawberry.enum
    class DifficultyOptions(models.IntegerChoices):
        EASY = 0
        NORMAL = 1
        HARD = 2
        VERYDIFFICULT = 3

    name = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=50)
    price_rp = models.IntegerField(choices=PriceRP.choices, default=PriceRP._975)
    price_be = models.IntegerField(choices=PriceBE.choices, default=PriceBE._6300)
    category = models.IntegerField(choices=Category.choices, default=Category.DAMAGE)
    damage_type = models.IntegerField(
        choices=DamageType.choices, default=DamageType.ATTACK_DAMAGE
    )
    difficulty = models.IntegerField(
        choices=DifficultyOptions.choices, default=DifficultyOptions.NORMAL
    )
    description = models.TextField(default="description of the item")
    is_freetoplay = models.BooleanField(default=False)
    disabled = models.BooleanField(default=False)
    release_date = models.DateTimeField(auto_now_add=True)
    abilities = models.ForeignKey(ChampionAbility, on_delete=models.CASCADE, null=True)
    skins = models.ForeignKey(ChampionSkin, on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return f"{self.name}"


class ChampionImage(models.Model):
    champion = models.ForeignKey(
        Champion, related_name="images", on_delete=models.CASCADE
    )
    type = models.ImageField(default="image 2.jpg")
    style = models.ImageField(default="image 2.jpg")
    image = models.ImageField(default="image 2.jpg")


class SkinOwnerShip(models.Model):
    player = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="skins",
        null=True,
    )
    skin = models.ForeignKey(ChampionSkin, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.IntegerField()
    payment_currency = models.IntegerField(
        choices=Player.PaymentCurrency.choices, default=Player.PaymentCurrency.RP
    )

    def __str__(self) -> str:
        return f"{self.player} owns {self.skin}"


class ChampionOwnerShip(models.Model):
    player = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="champions",
        null=True,
    )
    champion = models.ForeignKey(Champion, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.IntegerField()
    payment_currency = models.IntegerField(
        choices=Player.PaymentCurrency.choices, default=Player.PaymentCurrency.BE
    )

    def __str__(self) -> str:
        return f"{self.player} owns {self.champion}"
