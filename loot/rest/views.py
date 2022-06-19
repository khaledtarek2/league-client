from ..models import Loot
from .serializers import LootSerializer
from rest_framework import viewsets

class LootViewSet(viewsets.ModelViewSet):
    queryset = Loot.objects.all()
    serializer_class = LootSerializer
    permission_classes = []

