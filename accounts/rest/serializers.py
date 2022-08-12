from rest_framework import serializers
from loot.models import Loot, LootOwnerShip
from champions.models import Champion, ChampionOwnerShip, ChampionSkin, SkinOwnerShip
from loot.rest.serializers import LootSerializer
from champions.rest.serializers import (
    ChampionSerializer,
    ChampionSkinSerializer,
    EnumSerializer,
)
from ..models import Rank, Profile, PlayerSeasonGrade, Player, Message
from rest_framework.exceptions import ValidationError


class RankSerializer(serializers.ModelSerializer):
    mode = EnumSerializer(enum=Rank.Modes)
    rank = EnumSerializer(enum=Rank.Level)

    class Meta:
        model = Rank
        fields = ["id", "mode", "rank"]


class ProfileSerializer(serializers.ModelSerializer):
    rank = RankSerializer()

    class Meta:
        model = Profile
        fields = ["id", "rank", "honor_level"]

    def create(self, validated_data):
        rank_data = validated_data.pop("rank")
        rank = Rank.objects.create(**rank_data)
        return Profile.objects.create(**validated_data, rank=rank)


class LootOwnerShipSerializer(serializers.ModelSerializer):
    loot = LootSerializer()

    class Meta:
        model = LootOwnerShip
        fields = ["id", "player", "loot", "created_at", "paid"]

    # def create(self, validated_data):
    #     loot_data = validated_data.pop("loot")
    #     loot = Loot.objects.create(**loot_data)
    #     return LootOwnerShip.objects.create(**validated_data, loot=loot)


class SkinOwnerShipOutSerializer(serializers.ModelSerializer):
    skin = ChampionSkinSerializer()
    payment_currency = EnumSerializer(enum=Player.PaymentCurrency)

    class Meta:
        model = SkinOwnerShip
        fields = ["id", "player", "skin", "created_at", "paid", "payment_currency"]

    def create(self, validated_data):
        skin_data = validated_data.pop("skin")
        skin = ChampionSkin.objects.create(**skin_data)
        return SkinOwnerShip.objects.create(**validated_data, skin=skin)


class SkinOwnerShipSerializer(serializers.ModelSerializer):
    skin = serializers.PrimaryKeyRelatedField(queryset=ChampionSkin.objects.all())
    payment_currency = EnumSerializer(enum=Player.PaymentCurrency)

    class Meta:
        model = SkinOwnerShip
        fields = ["id", "player", "skin", "created_at", "paid", "payment_currency"]

    def create(self, validated_data):
        player_id = validated_data.get("player")
        skin_id = validated_data.get("skin")
        if SkinOwnerShip.objects.filter(player_id=player_id, skin_id=skin_id).exists():
            raise ValidationError({"message": "the skin aleady exists in your account"})
        return validated_data


class ChampionOwnerShipSerializer(serializers.ModelSerializer):
    champion = serializers.PrimaryKeyRelatedField(queryset=Champion.objects.all())
    payment_currency = EnumSerializer(enum=Player.PaymentCurrency)

    class Meta:
        model = ChampionOwnerShip
        fields = ["id", "player", "champion", "created_at", "paid", "payment_currency"]

    def create(self, validated_data):
        player_id = validated_data.get("player")
        champion_id = validated_data.get("champion")
        if ChampionOwnerShip.objects.filter(
            player_id=player_id, champion_id=champion_id
        ).exists():
            raise ValidationError(
                {"message": "the champion aleady exists in your account"}
            )
        return validated_data


class ChampionOwnerShipOutSerializer(serializers.ModelSerializer):
    payment_currency = EnumSerializer(enum=Player.PaymentCurrency)
    champion = ChampionSerializer()

    class Meta:
        model = ChampionOwnerShip
        fields = ["id", "player", "champion", "created_at", "paid", "payment_currency"]

    # def create(self, validated_data):
    #     champion = validated_data.pop("champion")
    #     # cos = champion.championownership_set(champion)
    #     champ_serializer = ChampionSerializer(champion)
    #     print(champ_serializer.data)
    #     # validated_data.champion = champ_serializer.data
    #     # validated_data.champion = champion
    #     return ChampionOwnerShip.objects.create(**validated_data, champion=champ_serializer.data)

    # def create(self, validated_data):
    #     champion_data = validated_data.pop("champion")
    #     abilities_data = champion_data.pop("abilities")
    #     skins_data = champion_data.pop("skins")
    #     abilities = ChampionAbility.objects.create(**abilities_data)
    #     skins = ChampionSkin.objects.create(**skins_data)
    #     champion = Champion.objects.create(**champion_data)
    #     champion.abilities = abilities
    #     champion.skins = skins
    #     return ChampionOwnerShip.objects.create(**validated_data, champion=champion)


class PlayerSerializer(serializers.ModelSerializer):
    champions = ChampionOwnerShipSerializer(many=True, read_only=True)
    skins = SkinOwnerShipSerializer(many=True, read_only=True)
    loots = LootOwnerShipSerializer(many=True, read_only=True)
    server = EnumSerializer(enum=Player.Server)

    class Meta:
        model = Player
        fields = [
            "is_online",
            "level",
            "server",
            "profile",
            "friends",
            "first_name",
            "last_name",
            "full_name",
            "champions",
            "skins",
            "loots",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "friends": {"read_only": True},
        }


class PlayerSeasonGradeSerializer(serializers.ModelSerializer):
    grade = EnumSerializer(enum=PlayerSeasonGrade.SeasonGrade)

    class Meta:
        model = PlayerSeasonGrade
        fields = ["id", "player", "champion", "grade", "obtained_at"]


class PlayerUpdateFriendsSerializer(serializers.Serializer):
    player = serializers.PrimaryKeyRelatedField(queryset=Player.objects.all())

    friends = serializers.PrimaryKeyRelatedField(
        queryset=Player.objects.prefetch_related("friends"), many=True
    )

    def create(self, validated_data):
        friends = validated_data.get("friends")
        player = validated_data.get("player")
        player.friends.set(friends)
        return validated_data


class PlayerAddFriendsSerializer(serializers.Serializer):
    player = serializers.PrimaryKeyRelatedField(queryset=Player.objects.all())

    friends = serializers.PrimaryKeyRelatedField(
        queryset=Player.objects.prefetch_related("friends"), many=True
    )

    def create(self, validated_data):
        friends = validated_data.get("friends")
        player = validated_data.get("player")
        player.friends.add(*friends)

        return validated_data


class PlayerRemoveFriendsSerializer(serializers.Serializer):

    player = serializers.PrimaryKeyRelatedField(queryset=Player.objects.all())
    friends = serializers.PrimaryKeyRelatedField(
        queryset=Player.objects.prefetch_related("friends"), many=True
    )

    def create(self, validated_data):
        friends = validated_data.get("friends")
        player = validated_data.get("player")
        player.friends.remove(*friends)

        return validated_data


class MessageSerializer(serializers.ModelSerializer):
    """For Serializing Message"""

    sender = serializers.SlugRelatedField(
        many=False, slug_field="username", queryset=Player.objects.all()
    )
    receiver = serializers.SlugRelatedField(
        many=False, slug_field="username", queryset=Player.objects.all()
    )

    class Meta:
        model = Message
        fields = ["sender", "receiver", "message", "timestamp"]
