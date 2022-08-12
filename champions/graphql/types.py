import strawberry
from .. import models


@strawberry.type
class ImageFieldUpload:
    url: str
    path: str


@strawberry.type
class ChampionMasteryImage:
    icon: ImageFieldUpload


@strawberry.type
class EternalGroupImage:
    icon: ImageFieldUpload


@strawberry.type
class EternalImage:
    icon: ImageFieldUpload


@strawberry.type
class ChampionAbilityImage:
    icon: ImageFieldUpload


@strawberry.type
class ChampionSkinImage:
    border: ImageFieldUpload
    look: ImageFieldUpload


@strawberry.type
class ChampionImage:
    type: ImageFieldUpload
    style: ImageFieldUpload
    image: ImageFieldUpload


@strawberry.type
class EternalGroup:
    id: strawberry.ID
    name: str
    is_unlocked: bool


@strawberry.type
class ChampionAbility:
    id: strawberry.ID
    key: int
    name: str
    is_ultimate: bool
    description: str


@strawberry.type
class ChampionSkin:
    id: strawberry.ID
    name: str
    skin_rarity: models.ChampionSkin.SkinRarity


@strawberry.type
class Champion:
    id: strawberry.ID
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
    abilities: ChampionAbility
    skins: ChampionSkin


@strawberry.type
class RegisteredPlayer:
    id: strawberry.ID
    email: str
    password: str
    username: str


@strawberry.type
class ChampionMastery:
    id: strawberry.ID
    points: int
    title: str
    player: RegisteredPlayer
    champion: Champion
    level: int = 1


@strawberry.type
class Eternal:
    id: strawberry.ID
    score: int
    name: str
    group: EternalGroup
    champion: Champion


@strawberry.type
class SkinOwnerShip:
    id: strawberry.ID
    player: RegisteredPlayer
    skin: ChampionSkin
    paid: int
    payment_currency: models.Player.PaymentCurrency


@strawberry.type
class ChampionOwnerShip:
    id: strawberry.ID
    player: RegisteredPlayer
    champion: Champion
    paid: int
    payment_currency: models.Player.PaymentCurrency
