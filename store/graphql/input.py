import strawberry
from .. import models
from strawberry.scalars import JSON


@strawberry.input
class ItemInput:
    name: str
    passive: str
    active: str
    category: models.Item.Category
    stats: JSON
