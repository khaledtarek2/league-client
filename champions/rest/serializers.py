from rest_framework import serializers
from ..models import Champion, ChampionAbility, ChampionMastery, ChampionSkin, EternalGroup, Eternal



class EternalGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = EternalGroup
        fields = ["id", 'name', 'is_unlocked']


class EternalSerializer(serializers.ModelSerializer):
    group = EternalGroupSerializer()
    class Meta:
        model = Eternal
        fields = ["id", 'score', 'name', 'group']

    def create(self, validated_data):
        group_data = validated_data.pop('group')
        group = EternalGroup.objects.create(**group_data)
        return Eternal.objects.create(**validated_data, group=group)
        


class EnumSerializer(serializers.ChoiceField):
    def __init__(self, enum, **kwargs):
        self.enum = enum
        
        super().__init__(enum, **kwargs)

    def to_representation(self, value):
        value = super().to_representation(value)
        return value.name

class ChampionSkinSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChampionSkin
        fields = ["id", 'name', 'skin_rarity']
    skin_rarity = EnumSerializer(enum=ChampionSkin.SkinRarity)


class ChampionAbilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ChampionAbility
        fields = ["id", 'key', 'name', 'is_ultimate', 'description', 'video_showcase']
        


class ChampionMasterySerializer(serializers.ModelSerializer):
    class Meta:
        model = ChampionMastery
        fields = ["id", 'points', 'title', 'level']


class ChampionSerializer(serializers.ModelSerializer):
    abilities = ChampionAbilitySerializer()
    skins =  serializers.SlugRelatedField(
        queryset= ChampionSkin.objects.all(),
        slug_field ='name'
     )
    category = EnumSerializer(enum=Champion.Category)
    damage_type = EnumSerializer(enum=Champion.DamageType)
    price_be = EnumSerializer(enum=Champion.PriceBE)
    price_rp = EnumSerializer(enum=Champion.PriceRP)
    difficulty = EnumSerializer(enum=Champion.DifficultyOptions)
    class Meta:
        model = Champion
        fields = ["id", 'name', 'title', 'price_rp', 'price_be', 'type', 'category',
                'damage_type', 'style', 'difficulty', 'description',
                'is_freetoplay', 'disabled', 'release_date', 'abilities', 'skins']


    def create(self, validated_data):
        abilities_data = validated_data.pop('abilities')
        abilities = ChampionAbility.objects.create(**abilities_data)
        return Champion.objects.create(**validated_data, abilities=abilities)

