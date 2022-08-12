from datetime import datetime
import typing
import strawberry

from champions.graphql.types import RegisteredPlayer
from .. import models
from strawberry.types import Info


@strawberry.type
class ImageFieldUpload:
    url: str
    path: str


@strawberry.type
class LootImage:
    image: ImageFieldUpload


@strawberry.type
class Loot:
    id: strawberry.ID
    name: str
    description: str
    price: int
    category: models.Loot.Category
    currency: models.Loot.Currency

    @strawberry.field
    def images(self, info: Info) -> typing.List[LootImage]:
        return self.images.all()


@strawberry.type
class LootOwnerShip:
    id: strawberry.ID
    player: RegisteredPlayer
    loot: Loot
    created_at: datetime
    paid: int
