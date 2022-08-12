from rest_framework.routers import DefaultRouter
from loot.rest.views import LootViewSet
from django.urls import include, path


router = DefaultRouter()

router.register(r"loot", LootViewSet, basename="loot")


urlpatterns = [path("", include(router.urls))]
