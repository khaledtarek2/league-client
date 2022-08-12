from rest_framework.routers import DefaultRouter
from store.rest.views import ItemViewSet
from django.urls import include, path

router = DefaultRouter()

router.register(r"items", ItemViewSet, basename="item")

urlpatterns = [path("", include(router.urls))]
