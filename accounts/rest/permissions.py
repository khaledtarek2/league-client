from rest_framework import permissions
from champions.models import ChampionSkin, SkinOwnerShip
from guardian.shortcuts import get_perms
from django.http import Http404

class IsPurchasableSkinOrReadOnly(permissions.DjangoObjectPermissions):
    def has_object_permission(self, request, view, owner_ship):
       pass
