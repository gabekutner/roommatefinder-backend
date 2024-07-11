from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

from .internal import internal_profiles
from .views import (
  profile_views, 
  swipe_views, 
  matching_views, 
  photo_views, 
  widgets_views,
  tokens
)

router = routers.DefaultRouter()

router.register(
  r"profiles",
  profile_views.ProfileViewSet,
  basename="profile",
)

router.register(
  r"photos",
  photo_views.PhotoViewSet,
  basename="photo",
)

router.register(
  r"matching-quizs",
  matching_views.RoommateQuizViewSet,
  basename="matching-quiz"
)

router.register(
  r"links",
  widgets_views.LinkViewSet,
  basename="link",
)

router.register(
  r"prompts",
  widgets_views.PromptViewSet,
  basename="prompt",
)
router.register(
  r"quotes",
  widgets_views.QuoteViewSet,
  basename="quote",
)

urlpatterns = [
  # internal admin actions - profiles
  path("internal/profiles/", internal_profiles.list_profiles, name="list_profiles"),
  path("internal/profiles/delete/<pk>/",
       internal_profiles.delete_profile,
       name="delete_profile"),

  # authentication
  path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
  path(
    "users/login/",
    tokens.MyTokenObtainPairView.as_view(),
    name="login",
  ),

  # ViewSets
  path("", include(router.urls)),
  path("swipe/", swipe_views.SwipeModelViewSet.as_view(), name="swipe"),
  path("swipe/<pk>/", swipe_views.SwipeDetailView.as_view(), name="swipe-profile")
]