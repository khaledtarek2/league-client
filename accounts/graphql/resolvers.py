import typing
import strawberry
from store.graphql.pagination import Connection, Cursor, Edge, PageInfo, build_item_cursor
from .types import Message, Player, PlayerSeasonGrade, Profile, Rank
from .. import models



def players(first: int = 10, after: typing.Optional[Cursor] = strawberry.UNSET) -> Connection[Player]:
    """
    A non-trivial implementation should efficiently fetch only
    the necessary books after the offset.
    For simplicity, here we build the list and then slice it accordingly
    """
    after = after if after is not strawberry.UNSET else None

    # Fetch the requested books plus one, just to calculate `has_next_page`
    
    
    players = models.Player.objects.all()[:first + 1]
    edges = [
    
        Edge(node=Player.from_db_model(player), cursor=build_item_cursor(player))
        for player in players
    ]

    return Connection(
        page_info=PageInfo(
            has_previous_page=False,
            has_next_page=len(players) > first,
            start_cursor=edges[0].cursor if edges else None,
            end_cursor=edges[-2].cursor if len(edges) > 1 else None,
        ),
        edges=edges[:-1]  # exclude last one as it was fetched to know if there is a next page
    )



async def player(id: strawberry.ID) -> Player:
    return models.Player.objects.get(id=id)


async def profiles() -> typing.List[Profile]:
    return models.Profile.objects.all()


async def profile(id: strawberry.ID) -> Profile:
    return models.Profile.objects.get(id=id)


async def ranks() -> typing.List[Rank]:
    return models.Rank.objects.all()


async def rank(id: strawberry.ID) -> Rank:
    return models.Rank.objects.get(id=id)


async def season_grades() -> typing.List[PlayerSeasonGrade]:
    return models.PlayerSeasonGrade.objects.all()


async def season_grade(id: strawberry.ID) -> PlayerSeasonGrade:
    return models.PlayerSeasonGrade.objects.get(id=id)


async def messages() -> typing.List[Message]:
    return models.Message.objects.all()


async def message(id: strawberry.ID) -> Message:
    return models.Message.objects.get(id=id)
