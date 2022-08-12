import strawberry
from .. import models


@strawberry.input
class ChampionMasteryImageInput:
    icon: str


@strawberry.input
class EternalGroupImageInput:
    icon: str


@strawberry.input
class EternalImageInput:
    icon: str


@strawberry.input
class ChampionAbilityImageInput:
    icon: str


@strawberry.input
class ChampionSkinImageInput:
    border: str
    look: str


@strawberry.input
class ChampionImageInput:
    type: str
    style: str
    image: str


@strawberry.input
class EternalGroupInput:
    name: str
    is_unlocked: bool


@strawberry.input
class ChampionAbilityInput:
    key: int
    name: str
    is_ultimate: bool
    description: str


@strawberry.input
class RegisterPlayerInput:
    email: str
    password: str
    username: str


@strawberry.input
class ChampionSkinInput:
    name: str
    skin_rarity: models.ChampionSkin.SkinRarity


@strawberry.input
class ChampionInput:
    name: str
    title: str
    price_rp: models.Champion.PriceRP
    price_be: models.Champion.PriceBE
    category: models.Champion.Category
    damage_type: models.Champion.DamageType
    difficulty: models.Champion.DifficultyOptions
    description: str
    is_freetoplay: bool
    disabled: bool
    abilities: ChampionAbilityInput
    skins: ChampionSkinInput


@strawberry.input
class EternalInput:
    score: int
    name: str
    group: EternalGroupInput
    champion: str


@strawberry.input
class ChampionMasteryInput:
    points: int
    title: str
    level: int
    player: str
    champion: str


@strawberry.input
class SkinOwnerShipInput:
    player: str
    skin: ChampionSkinInput
    paid: int
    payment_currency: models.Player.PaymentCurrency


@strawberry.input
class ChampionOwnerShipInput:
    player: str
    champion: str
    paid: int
    payment_currency: models.Player.PaymentCurrency
