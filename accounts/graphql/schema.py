import typing
import strawberry
from .input import (
    MessageInput,
    PlayerInput,
    PlayerSeasonGradeInput,
    ProfileInput,
    RankInput,
    RegisterPlayerInput,
    UpdateRankInput,
)
from .. import models
from . import resolvers
from .types import (
    Message,
    Player,
    PlayerAddRemoveFriend,
    PlayerSeasonGrade,
    Profile,
    Rank,
)
from django.core.validators import validate_email
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from champions import models as champion_models


def user_with_username_exists(username):
    return models.Player.objects.filter(username=username).exists()


def user_with_email_exists(email):
    return models.Player.objects.filter(email=email).exists()


def is_valid_email(email):
    validate_email(email)
    return True


def validate_player_input(player_input: PlayerInput):
    if not is_valid_email(player_input.email):
        raise ValidationError({"message": "Invaid email"})

    if user_with_email_exists(player_input.email):
        raise ValidationError({"message": "Email already in use"})

    if user_with_username_exists(player_input.username):
        raise ValidationError({"message": "Username is in use"})


@strawberry.type
class Query:
    players: typing.List[Player] = strawberry.field(resolver=resolvers.players)
    player: Player = strawberry.field(resolver=resolvers.player)
    profiles: typing.List[Profile] = strawberry.field(resolver=resolvers.profiles)
    profile: Profile = strawberry.field(resolver=resolvers.profile)
    ranks: typing.List[Rank] = strawberry.field(resolver=resolvers.ranks)
    rank: Rank = strawberry.field(resolver=resolvers.rank)
    season_grades: typing.List[Rank] = strawberry.field(
        resolver=resolvers.season_grades
    )
    season_grade: Rank = strawberry.field(resolver=resolvers.season_grade)
    messages: typing.List[Message] = strawberry.field(resolver=resolvers.messages)
    message: Message = strawberry.field(resolver=resolvers.message)


@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_rank(self, rank_input: RankInput) -> Rank:
        images = models.RankImage.objects.create(
            border=rank_input.images.border, icon=rank_input.images.icon
        )
        rank = models.Rank.objects.create()
        rank.images.add(images)
        return rank

    @strawberry.mutation
    def update_rank(self, id: strawberry.ID, rank_input: UpdateRankInput) -> Rank:
        rank_qs = models.Rank.objects.filter(id=id)
        rank_qs.update(mode=rank_input.mode, rank=rank_input.rank)
        rank = rank_qs.first()
        rank_images_qs = rank.images.filter()
        if rank_images_qs.exists():
            rank_images = rank_images_qs.first()
            rank.images.set([rank_images])
        else:
            created_rank_images = models.RankImage.objects.create(
                border=rank_input.images.border, icon=rank_input.images.icon
            )
            rank.images.set([created_rank_images])
        rank_images_qs.update(
            border=rank_input.images.border, icon=rank_input.images.icon
        )
        return rank

    @strawberry.mutation
    def create_profile(self, profile: ProfileInput) -> Profile:
        rank_images = models.RankImage.objects.create(
            icon=profile.rank.images.icon,
            border=profile.rank.images.border,
        )
        rank = models.Rank.objects.create()
        rank.images.add(rank_images)
        profile_image = models.ProfileImage.objects.create(trophy=profile.images.trophy)
        profile = models.Profile.objects.create(rank=rank)
        profile.images.add(profile_image)
        return profile

    @strawberry.mutation
    def update_profile(self, id: strawberry.ID, profile_input: ProfileInput) -> Profile:
        profile_qs = models.Profile.objects.filter(id=id)
        profile_qs.update(honor_level=profile_input.honor_level)
        profile = profile_qs.first()
        rank_qs = models.Rank.objects.filter(id=profile.rank.id)
        rank_qs.update(mode=profile_input.rank.mode, rank=profile_input.rank.rank)
        rank = rank_qs.first()
        rank_images_qs = rank.images.all()
        if rank_images_qs.exists():
            rank_images = rank_images_qs.first()
            rank.images.set([rank_images])
        else:
            created_rank_images = models.RankImage.objects.create(
                border=profile_input.rank.images.border,
                icon=profile_input.rank.images.icon,
            )
            rank.images.set([created_rank_images])
        rank_images_qs.update(
            border=profile_input.rank.images.border, icon=profile_input.rank.images.icon
        )

        profile_images_qs = profile.images.all()
        if profile_images_qs.exists():
            profile_images = profile_images_qs.first()
            profile.images.set([profile_images])
        else:
            created_profile_images = models.ProfileImage.objects.create(
                banner=profile_input.images.banner,
                trophy=profile_input.images.trophy,
                background_picture=profile_input.images.background_picture,
            )
            profile.images.set([created_profile_images])
        profile_images_qs.update(
            banner=profile_input.images.banner,
            trophy=profile_input.images.trophy,
            background_picture=profile_input.images.background_picture,
        )
        profile.refresh_from_db()
        return profile

    @strawberry.mutation
    def create_player(self, player_input: PlayerInput) -> Player:
        validate_player_input(player_input)
        rank_images = models.RankImage.objects.create(
            icon=player_input.profile.rank.images.icon,
            border=player_input.profile.rank.images.border,
        )

        rank = models.Rank.objects.create()
        rank.images.add(rank_images)
        profile_image = models.ProfileImage.objects.create(
            trophy=player_input.profile.images.trophy,
            banner=player_input.profile.images.banner,
        )
        profile = models.Profile.objects.create(rank=rank)
        profile.images.add(profile_image)
        player_image = models.PlayerImage.objects.create(icon=player_input.images.icon)

        player = models.Player.objects.create_user(
            first_name=player_input.first_name,
            last_name=player_input.last_name,
            level=player_input.level,
            server=player_input.server,
            profile=profile,
            email=player_input.email,
            username=player_input.username,
            password=player_input.password,
        )

        player.images.add(player_image)

        return player

    @strawberry.mutation
    def update_player(self, id: strawberry.ID, player_input: PlayerInput) -> Player:
        validate_player_input(player_input)
        player = models.Player.objects.get(pk=id)
        player.profile.rank.mode = player_input.profile.rank.mode
        player.profile.honor_level = player_input.profile.honor_level
        player.profile.rank.rank = player_input.profile.rank.rank
        try:
            profile_image = player.profile.images.get()
        except:
            raise ObjectDoesNotExist("no profile images attached")
        profile_image.banner = player_input.profile.images.banner
        profile_image.trophy = player_input.profile.images.trophy
        profile_image.background_picture = (
            player_input.profile.images.background_picture
        )
        try:
            rank_image = player.profile.rank.images.get()
        except:
            raise ObjectDoesNotExist("no rank images attached")
        rank_image.icon = player_input.profile.rank.images.icon
        rank_image.border = player_input.profile.rank.images.border
        player.profile.rank.images.set([rank_image])
        player.profile.images.set([profile_image])
        try:
            player_image = player.images.get()
        except:
            raise ObjectDoesNotExist("no player images attached")
        profile_image.save()
        rank_image.save()
        player.first_name = player_input.first_name
        player.username = player_input.username
        player.last_name = player_input.last_name
        player.level = player_input.level
        player.server = player_input.server
        # player.profile.honor_level = player_input.profile.honor_level
        # player.profile.rank.mode = player_input.profile.rank.mode
        # player.profile.rank.rank = player_input.profile.rank.rank
        player.profile.save()
        player.profile.rank.save()
        player.email = player_input.email
        player.password = player_input.password
        player_image.icon = player_input.images.icon
        player.images.set([player_image])
        player_image.save()
        player.save()
        return player

    @strawberry.mutation
    def register_player(self, player_input: RegisterPlayerInput) -> Player:
        validate_player_input(player_input)
        rank_images = models.RankImage.objects.create()
        rank = models.Rank.objects.create()
        rank.images.add(rank_images)
        profile_image = models.ProfileImage.objects.create()
        player_image = models.PlayerImage.objects.create()
        profile = models.Profile.objects.create(rank=rank)
        profile.images.add(profile_image)

        player = models.Player.objects.create_user(
            email=player_input.email,
            username=player_input.username,
            password=player_input.password,
            profile=profile,
        )
        player.images.add(player_image)
        return player

    @strawberry.mutation
    def update_registered_player(
        self, id: strawberry.ID, player_input: RegisterPlayerInput
    ) -> Player:
        validate_player_input(player_input)
        player_qs = models.Player.objects.filter(pk=id)
        player = player_qs.first()
        try:
            player_image = player.images.get()
        except:
            raise ObjectDoesNotExist("no player images to update")
        player_qs.update(
            email=player_input.email,
            username=player_input.username,
            password=player_input.password,
        )
        player_image.icon = player_input.icon
        player.images.set([player_image])
        player_image.save()
        return player

    @strawberry.mutation
    def add_friend(self, username: str) -> PlayerAddRemoveFriend:
        player = models.Player.objects.get(username=username)
        friend = models.Player.objects.prefetch_related("friends").get(
            username=username
        )

        player.friends.add(friend)
        return player

    @strawberry.mutation
    def remove_friend(self, username: str) -> PlayerAddRemoveFriend:
        player = models.Player.objects.get(username=username)
        friend = models.Player.objects.prefetch_related("friends").get(
            username=username
        )
        player.friends.remove(friend)
        return player

    @strawberry.mutation
    def create_message(self, message_input: MessageInput) -> Message:
        sender = models.Player.objects.get(email=message_input.sender)
        receiver = models.Player.objects.get(email=message_input.receiver)
        message = models.Message.objects.create(
            sender=sender,
            receiver=receiver,
            message=message_input.message,
            is_read=message_input.is_read,
        )
        return message

    @strawberry.mutation
    def update_message(self, id: strawberry.ID, message_input: MessageInput) -> Message:
        message_qs = models.Message.objects.filter(id=id)
        message_qs.update(message=message_input.message)
        return message_qs.first()

    @strawberry.mutation
    def create_season_grade(
        self, id: strawberry.ID, player_sg_input: PlayerSeasonGradeInput
    ) -> PlayerSeasonGrade:
        player = models.Player.objects.get(username=player_sg_input.player)
        champion = champion_models.Champion.objects.get(pk=id)
        return models.PlayerSeasonGrade.objects.create(
            player=player, champion=champion, grade=player_sg_input.grade
        )

    @strawberry.mutation
    def update_season_grade(
        self, id: strawberry.ID, player_sg_input: PlayerSeasonGradeInput
    ) -> PlayerSeasonGrade:
        season_grade_qs = models.PlayerSeasonGrade.objects.filter(id=id)
        season_grade_qs.update(grade=player_sg_input.grade)
        return season_grade_qs.first()
