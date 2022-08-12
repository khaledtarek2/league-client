import strawberry
from .. import models


@strawberry.input
class LootInput:
    name: str
    description: str
    price: int
    category: models.Loot.Category
    currency: models.Loot.Currency
    image: str


@strawberry.input
class LootOwnerShipInput:
    player: str
    loot: LootInput
    paid: int
