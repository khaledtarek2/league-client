from rest_framework import serializers
from ..models import Loot
from champions.rest.serializers import EnumSerializer


class LootSerializer(serializers.ModelSerializer):
    category = EnumSerializer(enum=Loot.Category)
    currency = EnumSerializer(enum=Loot.Currency)

    class Meta:
        model = Loot
        fields = ["id", "name", "description", "price", "category", "currency"]
