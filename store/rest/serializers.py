from rest_framework import serializers
from ..models import Item
from champions.rest.serializers import EnumSerializer


class ItemSerializer(serializers.ModelSerializer):
    type = EnumSerializer(enum=Item.Type)
    class Meta:
        model = Item
        fields = ["id", 'stats', 'passive', 'active', 'type']
        

