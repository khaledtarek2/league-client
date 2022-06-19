from champions.rest.views import (ChampionAbilityViewSet, ChampionMasteryViewSet,
                        ChampionSkinViewSet, ChampionViewSet, EternalGroupViewSet, EternalViewSet)
from rest_framework.routers import DefaultRouter

from django.urls import include, path

router = DefaultRouter()

router.register(r'skins', ChampionSkinViewSet, basename='skin')
router.register(r'champions', ChampionViewSet, basename='champion')
router.register(r'abilities', ChampionAbilityViewSet, basename='ability')
router.register(r'mastries', ChampionMasteryViewSet, basename='mastery')
router.register(r'eternals', EternalViewSet, basename='eternal')
router.register(r'eternals_group', EternalGroupViewSet, basename='eternals_group')

urlpatterns = [
    path('', include(router.urls))
]