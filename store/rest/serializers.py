from rest_framework import serializers
from ..models import Item
from champions.rest.serializers import EnumSerializer


class ItemSerializer(serializers.ModelSerializer):
    category = EnumSerializer(enum=Item.Category)

    class Meta:
        model = Item
        fields = ["id", "name", "stats", "passive", "active", "category"]
