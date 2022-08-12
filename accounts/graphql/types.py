from datetime import datetime
import typing
import strawberry
from django.core.exceptions import ValidationError
from .. import models
from strawberry.types import Info
from champions.graphql.types import Champion


@strawberry.type
class ImageFieldUpload:
    url: str
    path: str


@strawberry.type
class RankImage:
    id: strawberry.ID
    icon: ImageFieldUpload
    border: ImageFieldUpload


@strawberry.type
class Rank:
    id: strawberry.ID
    mode: models.Rank.Modes
    rank: models.Rank.Level

    @strawberry.field
    def images(self, info: Info) -> typing.List[RankImage]:
        return self.images.all()


@strawberry.type
class PlayerImage:
    id: strawberry.ID
    icon: ImageFieldUpload


@strawberry.type
class ProfileImage:
    id: strawberry.ID
    trophy: ImageFieldUpload
    banner: ImageFieldUpload
    background_picture: ImageFieldUpload


@strawberry.type
class Profile:
    id: strawberry.ID
    rank: Rank
    honor_level: int = 2

    @strawberry.field
    def images(self, info: Info) -> typing.List[ProfileImage]:
        return self.images.all()


@strawberry.type
class Friends:
    id: strawberry.ID
    is_online: bool
    level: int
    server: models.Player.Server
    profile: Profile
    first_name: str
    last_name: str
    username: str

    @strawberry.field
    def images(self, info: Info) -> typing.List[PlayerImage]:
        return self.images.all()


@strawberry.type
class Player:
    id: strawberry.ID
    is_online: bool
    level: int
    server: models.Player.Server
    profile: Profile
    first_name: str
    last_name: str
    email: str
    username: str

    @strawberry.field
    def all_friends(self, info: Info) -> typing.List[Friends]:
        try:
            return self.friends.all()
        except:
            raise ValidationError({"message": "friends do not exist in this player"})

    @strawberry.field
    def all_images(self, info: Info) -> typing.List[PlayerImage]:
        try:
            return self.images.all()
        except:
            raise ValidationError({"message": "friends do not exist in this player"})

    @classmethod
    def from_db_model(cls, instance):
        """Adapt this method with logic to map your orm instance to a strawberry decorated class"""
        return cls(id=instance.id, is_online=instance.is_online, level=instance.level, server=instance.server,
                   profile=instance.profile, first_name=instance.first_name, last_name=instance.last_name,
                   email=instance.email, username=instance.username)

    @strawberry.field
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"




@strawberry.type
class FriendrAddRemove:
    id: strawberry.ID
    username: str


@strawberry.type
class PlayerAddRemoveFriend:
    id: strawberry.ID
    username: str

    @strawberry.field
    def friends(self, info: Info) -> typing.List[FriendrAddRemove]:
        return self.friends.all()


@strawberry.type
class Message:
    id: strawberry.ID
    sender: str
    receiver: str
    timestamp: datetime
    is_read: bool
    message: str


@strawberry.type
class RegisteredPlayer:
    id: strawberry.ID
    email: str
    username: str


@strawberry.type
class PlayerSeasonGrade:
    id: strawberry.ID
    grade: models.PlayerSeasonGrade.SeasonGrade
    player: RegisteredPlayer
    champion: Champion
