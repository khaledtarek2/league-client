from turtle import title
import typing
import strawberry

from .input import (
    ChampionInput,
    ChampionAbilityInput,
    ChampionMasteryInput,
    ChampionOwnerShipInput,
    ChampionSkinInput,
    EternalGroupInput,
    EternalInput,
    SkinOwnerShipInput,
)
from .. import models
from accounts import models as accountmodels
from . import resolvers
from .types import (
    ChampionOwnerShip,
    EternalGroup,
    Eternal,
    Champion,
    ChampionAbility,
    ChampionMastery,
    ChampionOwnerShip,
    ChampionSkin,
    SkinOwnerShip,
)
from graphql import GraphQLError, ValidationRule


@strawberry.type
class Query:
    champions: typing.List[Champion] = strawberry.field(resolver=resolvers.champions)
    champion: Champion = strawberry.field(resolver=resolvers.champion)
    champion_skins: typing.List[ChampionSkin] = strawberry.field(
        resolver=resolvers.champion_skins
    )
    champion_skin: ChampionSkin = strawberry.field(resolver=resolvers.champion_skin)
    eternals: typing.List[Eternal] = strawberry.field(resolver=resolvers.eternals)
    eternal: Eternal = strawberry.field(resolver=resolvers.eternal)
    eternal_groups: typing.List[EternalGroup] = strawberry.field(
        resolver=resolvers.eternal_groups
    )
    eternal_group: EternalGroup = strawberry.field(resolver=resolvers.eternal_group)
    champion_ownerships: typing.List[ChampionOwnerShip] = strawberry.field(
        resolver=resolvers.champion_ownerships
    )
    champion_ownership: ChampionOwnerShip = strawberry.field(
        resolver=resolvers.champion_ownership
    )
    skin_ownerships: typing.List[SkinOwnerShip] = strawberry.field(
        resolver=resolvers.skin_ownerships
    )
    skin_ownership: SkinOwnerShip = strawberry.field(resolver=resolvers.skin_ownership)
    champion_mastries: typing.List[ChampionMastery] = strawberry.field(
        resolver=resolvers.champion_mastries
    )
    champion_mastry: ChampionMastery = strawberry.field(
        resolver=resolvers.champion_mastry
    )


@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_skin(self, skin: ChampionSkinInput) -> ChampionSkin:
        return models.ChampionSkin.objects.create(
            name=skin.name, skin_rarity=skin.skin_rarity
        )

    @strawberry.mutation
    def create_eternal_group(self, eternal_group: EternalGroupInput) -> EternalGroup:
        return models.EternalGroup.objects.create(
            name=eternal_group.name,
            is_unlocked=eternal_group.is_unlocked,
        )

    @strawberry.mutation
    def create_eternal(self, eternal: EternalInput) -> Eternal:
        group = models.EternalGroup.objects.get(name=eternal.group.name)
        champion = models.Champion.objects.get(name=eternal.champion)
        return models.Eternal.objects.create(
            name=eternal.name, score=eternal.score, group=group, champion=champion
        )

    @strawberry.mutation
    def create_mastery(self, mastery: ChampionMasteryInput) -> ChampionMastery:
        player = accountmodels.Player.objects.get(username=mastery.player)
        champion = models.Champion.objects.get(
            name=mastery.champion,
        )
        return models.ChampionMastery.objects.create(
            points=mastery.points,
            player=player,
            champion=champion,
        )

    @strawberry.mutation
    def create_ability(self, ability: ChampionAbilityInput) -> ChampionAbility:
        return models.ChampionAbility.objects.create(
            name=ability.name,
            key=ability.key,
            description=ability.description,
            is_ultimate=ability.is_ultimate,
        )

    @strawberry.mutation
    def create_champion(self, champion: ChampionInput) -> Champion:
        ability = models.ChampionAbility.objects.create(
            name=champion.abilities.name,
            key=champion.abilities.key,
            description=champion.abilities.description,
            is_ultimate=champion.abilities.is_ultimate,
        )
        champion_skin = models.ChampionSkin.objects.create(
            name=champion.skins.name, skin_rarity=champion.skins.skin_rarity
        )
        champion = models.Champion.objects.create(
            name=champion.name,
            title=champion.title,
            price_rp=champion.price_rp,
            price_be=champion.price_be,
            category=champion.category,
            damage_type=champion.damage_type,
            difficulty=champion.difficulty,
            description=champion.description,
            is_freetoplay=champion.is_freetoplay,
            disabled=champion.disabled,
            abilities=ability,
            skins=champion_skin,
        )
        return champion

    @strawberry.mutation
    def create_skin(self, skin: ChampionSkinInput) -> ChampionSkin:
        return models.ChampionSkin.objects.create(
            name=skin.name, skin_rarity=skin.skin_rarity
        )

    @strawberry.mutation
    def champion_ownership(
        self, champion_ownership: ChampionOwnerShipInput
    ) -> ChampionOwnerShip:
        player = models.Player.objects.get(username=champion_ownership.player)
        champion = models.Champion.objects.get(name=champion_ownership.champion)
        return models.ChampionOwnerShip.objects.create(
            paid=champion_ownership.paid,
            payment_currency=champion_ownership.payment_currency,
            player=player,
            champion=champion,
        )

    @strawberry.mutation
    def skin_ownership(self, skin_ownership: SkinOwnerShipInput) -> SkinOwnerShip:
        player = models.Player.objects.get(username=skin_ownership.player)
        skin = models.ChampionSkin.objects.get(name=skin_ownership.skin.name)
        return models.SkinOwnerShip.objects.create(
            paid=skin_ownership.paid,
            payment_currency=skin_ownership.payment_currency,
            player=player,
            skin=skin,
        )
