import strawberry
from .. import models
from strawberry.scalars import JSON


@strawberry.type
class Item:
    id: strawberry.ID
    name: str
    passive: str
    active: str
    category: models.Item.Category
    stats: JSON

    @classmethod
    def from_db_model(cls, instance):
        """Adapt this method with logic to map your orm instance to a strawberry decorated class"""
        return cls(id=instance.id, name=instance.name, passive=instance.passive, active=instance.active,
                   category=instance.category, stats=instance.stats)
