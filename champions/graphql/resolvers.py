import strawberry
from .. import models


async def champions():
    return models.Champion.objects.all()


async def champion(id: strawberry.ID):
    return models.Champion.objects.get(id=id)


async def champion_skins():
    return models.ChampionSkin.objects.all()


async def champion_skin(id: strawberry.ID):
    return models.ChampionSkin.objects.get(id=id)


async def champion_ownerships():
    return models.ChampionOwnerShip.objects.all()


async def champion_ownership(id: strawberry.ID):
    return models.ChampionOwnerShip.objects.get(id=id)


async def skin_ownerships():
    return models.SkinOwnerShip.objects.all()


async def skin_ownership(id: strawberry.ID):
    return models.SkinOwnerShip.objects.get(id=id)


async def champion_mastries():
    return models.ChampionMastery.objects.all()


async def champion_mastry(id: strawberry.ID):
    return models.ChampionMastery.objects.get(id=id)


async def eternal_groups():
    return models.EternalGroup.objects.all()


async def eternal_group(id: strawberry.ID):
    return models.EternalGroup.objects.get(id=id)


async def eternals():
    return models.Eternal.objects.all()


async def eternal(id: strawberry.ID):
    return models.Eternal.objects.get(id=id)
