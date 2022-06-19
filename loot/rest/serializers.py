from rest_framework import serializers
from ..models import Loot
from champions.rest.serializers import EnumSerializer


class LootSerializer(serializers.ModelSerializer):
    type = EnumSerializer(enum=Loot.LootType)
    currency = EnumSerializer(enum=Loot.LootCurrency)
    class Meta:
        model = Loot
        fields = ["id", 'name', 'description', 'price', 'type', 'currency']
        

