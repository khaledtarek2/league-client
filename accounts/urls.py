from accounts.rest.views import (
    MessageViewSet,
    PlayerAddFriendsView,
    PlayerRemoveFriendsView,
    PlayerViewSet,
    PlayerUpdateFriendsView,
    ProfileViewSet,
    PlayerSeasonGradeyViewSet,
    RankViewSet,
    LootOwnerShipViewSet,
    ChampionOwnerShipViewSet,
    SkinOwnerShipViewSet,
)
from rest_framework.routers import DefaultRouter
from django.urls import include, path
from . import views
from django.contrib.auth import logout

router = DefaultRouter()


router.register(r"players", PlayerViewSet, basename="player")
router.register(r"profiles", ProfileViewSet, basename="profile")
router.register(r"player_season_grade", PlayerSeasonGradeyViewSet, basename="player_sg")
router.register(r"ranks", RankViewSet, basename="rank")
router.register(r"loot_ownerships", LootOwnerShipViewSet, basename="loot_os")
router.register(
    r"champion_ownerships", ChampionOwnerShipViewSet, basename="champion_os"
)
router.register(r"skin_ownerships", SkinOwnerShipViewSet, basename="skin_os")
router.register(r"messages", MessageViewSet, basename="message")

app_name = "accounts"

urlpatterns = [
    path("", include(router.urls)),
    path("player_update_friends/<int:pk>", view=PlayerUpdateFriendsView.as_view()),
    path("player_add_friends/<int:pk>", view=PlayerAddFriendsView.as_view()),
    path("player_remove_friends/<int:pk>", view=PlayerRemoveFriendsView.as_view()),
    path("index/", views.index, name="index"),
    path("register/", views.register_view, name="register"),
    path("chat/", views.chat_view, name="chat"),
    path("api/messages/<int:sender>/<int:receiver>/",
        views.message_view,
        name="message-detail",
    ),
    path("logout", views.logout_view, name="logout"),
]
