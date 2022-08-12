from ..models import (
    Eternal,
    EternalGroup,
    SkinOwnerShip,
    Champion,
    ChampionAbility,
    ChampionMastery,
    ChampionSkin,
    ChampionOwnerShip,
)
from .serializers import (
    ChampionSerializer,
    ChampionAbilitySerializer,
    ChampionMasterySerializer,
    ChampionSkinSerializer,
    EternalGroupSerializer,
    EternalSerializer,
)
from rest_framework import viewsets


class ChampionViewSet(viewsets.ModelViewSet):
    queryset = Champion.objects.all()
    serializer_class = ChampionSerializer
    permission_classes = []


class ChampionAbilityViewSet(viewsets.ModelViewSet):
    queryset = ChampionAbility.objects.all()
    serializer_class = ChampionAbilitySerializer
    permission_classes = []


class ChampionMasteryViewSet(viewsets.ModelViewSet):
    queryset = ChampionMastery.objects.all()
    serializer_class = ChampionMasterySerializer
    permission_classes = []


class ChampionSkinViewSet(viewsets.ModelViewSet):
    queryset = ChampionSkin.objects.all()
    serializer_class = ChampionSkinSerializer
    permission_classes = []


class EternalViewSet(viewsets.ModelViewSet):
    queryset = Eternal.objects.all()
    serializer_class = EternalSerializer
    permission_classes = []


class EternalGroupViewSet(viewsets.ModelViewSet):
    queryset = EternalGroup.objects.all()
    serializer_class = EternalGroupSerializer
    permission_classes = []
