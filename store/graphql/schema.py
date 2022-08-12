import typing
import strawberry
from .input import ItemInput
from .. import models
from . import resolvers
from .types import Item


@strawberry.type
class Query:
    items: typing.List[Item] = strawberry.field(resolver=resolvers.items)
    item: Item = strawberry.field(resolver=resolvers.item)


@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_item(self, item: ItemInput) -> Item:
        return models.Item.objects.create(
            name=item.name,
            stats=item.stats,
            passive=item.passive,
            active=item.active,
            category=item.category,
        )

    @strawberry.mutation
    def update_item(self, item_id: strawberry.ID, item_input: ItemInput) -> Item:
        item_qs = models.Item.objects.filter(pk=item_id)
        item_qs.update(
            name=item_input.name,
            stats=item_input.stats,
            passive=item_input.passive,
            active=item_input.active,
            category=item_input.category,
        )
        return item_qs.first()
