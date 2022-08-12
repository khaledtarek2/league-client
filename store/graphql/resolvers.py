import base64
from typing import Optional
import strawberry
from .pagination import Connection, Cursor, Edge, PageInfo, build_item_cursor
from .. import models
from . import types
from django.core.exceptions import ValidationError


# async def get_items(info):
#     return models.Item.objects.all()


async def item(id: strawberry.ID):
    return models.Item.objects.get(id=id)


def items(first: int = 10, after: Optional[Cursor] = strawberry.UNSET) -> Connection[types.Item]:
    """
    A non-trivial implementation should efficiently fetch only
    the necessary books after the offset.
    For simplicity, here we build the list and then slice it accordingly
    """
    after = after if after is not strawberry.UNSET else None

    # Fetch the requested books plus one, just to calculate `has_next_page`
    try:
        _, pk = base64.b64decode(after).decode().split('::')
    except ValueError:
        raise ValidationError('invalid id')

    items = models.Item.objects.all().order_by('-id').filter(pk__gte=pk)[:first+1]

    edges = [

        Edge(node=types.Item.from_db_model(item), cursor=build_item_cursor(item))
        for item in items
    ]

    return Connection(
        page_info=PageInfo(
            has_previous_page=False,
            has_next_page=len(items) > first,
            start_cursor=edges[0].cursor if edges else None,
            end_cursor=edges[-2].cursor if len(edges) > 1 else None,
        ),
        edges=edges[:-1]  # exclude last one as it was fetched to know if there is a next page
    )
