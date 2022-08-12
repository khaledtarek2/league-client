from ..models import Rank, Profile, Player, PlayerSeasonGrade, Message
from .serializers import (
    PlayerAddFriendsSerializer,
    PlayerRemoveFriendsSerializer,
    PlayerUpdateFriendsSerializer,
    RankSerializer,
    ProfileSerializer,
    PlayerSerializer,
    PlayerSeasonGradeSerializer,
    LootOwnerShipSerializer,
    ChampionOwnerShipSerializer,
    SkinOwnerShipOutSerializer,
    SkinOwnerShipSerializer,
    ChampionOwnerShipOutSerializer,
    MessageSerializer,
)
from champions.models import SkinOwnerShip, ChampionOwnerShip
from rest_framework import viewsets, status
from loot.models import LootOwnerShip
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response


class SkinOwnerShipViewSet(viewsets.ModelViewSet):
    queryset = SkinOwnerShip.objects.all()
    serializer_class = SkinOwnerShipSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        saved = serializer.save()
        headers = self.get_success_headers(serializer.data)
        SOS_serializer = SkinOwnerShipOutSerializer(saved)
        return Response(
            SOS_serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class ChampionOwnerShipViewSet(viewsets.ModelViewSet):
    queryset = ChampionOwnerShip.objects.all()
    serializer_class = ChampionOwnerShipSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        saved = serializer.save()
        headers = self.get_success_headers(serializer.data)
        COS_serializer = ChampionOwnerShipOutSerializer(saved)
        return Response(
            COS_serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class RankViewSet(viewsets.ModelViewSet):
    queryset = Rank.objects.all()
    serializer_class = RankSerializer
    permission_classes = []


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = []


class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    permission_classes = []


class PlayerSeasonGradeyViewSet(viewsets.ModelViewSet):
    queryset = PlayerSeasonGrade.objects.all()
    serializer_class = PlayerSeasonGradeSerializer
    permission_classes = []


class LootOwnerShipViewSet(viewsets.ModelViewSet):
    queryset = LootOwnerShip.objects.all()
    serializer_class = LootOwnerShipSerializer
    permission_classes = []


class PlayerUpdateFriendsView(CreateAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerUpdateFriendsSerializer
    authentication_classes = []
    permission_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        player = self.get_object()
        player_serializer = PlayerSerializer(player)
        return Response(
            player_serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class PlayerAddFriendsView(PlayerUpdateFriendsView):
    queryset = Player.objects.all()
    serializer_class = PlayerAddFriendsSerializer
    authentication_classes = []
    permission_classes = []


class PlayerRemoveFriendsView(PlayerUpdateFriendsView):
    queryset = Player.objects.all()
    serializer_class = PlayerRemoveFriendsSerializer
    authentication_classes = []
    permission_classes = []


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = []
