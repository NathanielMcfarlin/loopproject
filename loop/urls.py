"""
URL configuration for loop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from loopapi.views import (
    reactionViewSet,
    UserViewSet,
    PlatformPostViewSet,
    GamePostViewSet,
    GameViewSet,
    PlatformViewSet,
    PostReactionViewSet,
    LikesViewSet
)


router = DefaultRouter(trailing_slash=False)
router.register(r"reactions", reactionViewSet, "reaction")
router.register(r"post_reactions", PostReactionViewSet, "post_reaction")
router.register(r"users", UserViewSet, "user")
router.register(r"platform_posts", PlatformPostViewSet, "post")
router.register(r"game_posts", GamePostViewSet, "post")
router.register(r"games", GameViewSet, "game")
router.register(r"platforms", PlatformViewSet, "platform")
router.register(r'likes', LikesViewSet, "likes")

urlpatterns = [
    path("", include(router.urls)),
    path("login", UserViewSet.as_view({"post": "user_login"}), name="login"),
    path(
        "register", UserViewSet.as_view({"post": "register_account"}), name="register"
    )
]