import strawberry
from .. import models


@strawberry.input
class RankImageInput:
    icon: str
    border: str


@strawberry.input
class PlayerImageInput:
    icon: str


@strawberry.input
class ProfileImageInput:
    trophy: str
    banner: str
    background_picture: str


@strawberry.input
class RankInput:
    images: RankImageInput


@strawberry.input
class UpdateRankInput:
    images: RankImageInput
    mode: models.Rank.Modes
    rank: models.Rank.Level


@strawberry.input
class ProfileInput:
    rank: UpdateRankInput
    images: ProfileImageInput
    honor_level: int


@strawberry.input
class FriendsInput:
    is_online: bool
    level: int
    server: models.Player.Server
    profile: ProfileInput
    first_name: str
    last_name: str
    username: str


@strawberry.input
class PlayerInput:
    is_online: bool
    level: int
    server: models.Player.Server
    profile: ProfileInput
    first_name: str
    last_name: str
    images: PlayerImageInput
    email: str
    password: str
    username: str


@strawberry.input
class RegisterPlayerInput:
    email: str
    password: str
    username: str
    icon: str


@strawberry.input
class MessageInput:
    sender: str
    receiver: str
    message: str
    is_read: bool


@strawberry.input
class PlayerSeasonGradeInput:
    grade: models.PlayerSeasonGrade.SeasonGrade
    player: str
