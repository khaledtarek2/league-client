import strawberry
from store.graphql.schema import Mutation, Query as StoreQuery
from store.graphql.schema import Mutation as StoreMutation
from loot.graphql.schema import Query as LootQuery
from loot.graphql.schema import Mutation as LootMutation
from accounts.graphql.schema import Query as AccountsQuery
from accounts.graphql.schema import Mutation as AccountsMutation
from champions.graphql.schema import Query as ChampionsQuery
from champions.graphql.schema import Mutation as ChampionsMutation


@strawberry.type
class Query(StoreQuery, LootQuery, AccountsQuery, ChampionsQuery):
    pass


@strawberry.type
class Mutation(StoreMutation, LootMutation, AccountsMutation, ChampionsMutation):
    pass


schema = strawberry.Schema(query=Query, mutation=Mutation)
