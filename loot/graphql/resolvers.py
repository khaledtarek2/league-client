import strawberry
from .types import LootOwnerShip
from .. import models


async def get_all_loot():
    return models.Loot.objects.all()


async def get_loot_by_id(id: strawberry.ID):
    return models.Loot.objects.get(id=id)


async def loot_ownerships():
    return models.LootOwnerShip.objects.all()


async def loot_ownership(id: strawberry.ID) -> LootOwnerShip:
    return models.LootOwnerShip.objects.get(pk=id)
