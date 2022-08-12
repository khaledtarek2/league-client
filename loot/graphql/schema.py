import typing
import strawberry
from .. import models
from . import resolvers
from accounts import models as account_models
from .types import Loot, LootOwnerShip
from .input import LootInput, LootOwnerShipInput


@strawberry.type
class Query:
    all_loot: typing.List[Loot] = strawberry.field(resolver=resolvers.get_all_loot)
    loot: Loot = strawberry.field(resolver=resolvers.get_loot_by_id)
    all_loot_os: typing.List[LootOwnerShip] = strawberry.field(
        resolver=resolvers.loot_ownerships
    )
    loot_os: LootOwnerShip = strawberry.field(resolver=resolvers.loot_ownership)


@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_loot(self, loot_input: LootInput) -> Loot:
        image = models.LootImage.objects.create(image=loot_input.image)
        loot = models.Loot.objects.create(
            name=loot_input.name,
            description=loot_input.description,
            price=loot_input.price,
            category=loot_input.category,
            currency=loot_input.currency,
        )
        loot.images.add(image)
        return loot

    @strawberry.mutation
    def create_loot_os(self, loot_os_input: LootOwnerShipInput) -> LootOwnerShip:
        loot = models.Loot.objects.get(name=loot_os_input.loot.name)
        player = account_models.Player.objects.get(username=loot_os_input.player)
        return models.LootOwnerShip.objects.create(
            paid=loot_os_input.paid,
            player=player,
            loot=loot,
        )

    @strawberry.mutation
    def update_loot(self, id: strawberry.ID, loot_input: LootInput) -> Loot:
        loot_qs = models.Loot.objects.filter(pk=id)
        loot = loot_qs.first()
        image = loot.images.get()
        loot_qs.update(
            name=loot_input.name,
            description=loot_input.description,
            price=loot_input.price,
            category=loot_input.category,
            currency=loot_input.currency,
        )
        image.image = loot_input.image
        loot.images.set([image])
        image.save()
        return loot
