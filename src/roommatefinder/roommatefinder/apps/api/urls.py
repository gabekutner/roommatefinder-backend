# -*- coding: utf-8 -*-
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

from .internal import internal_profiles
from .views import (
  profile_views, 
  matching_views, 
  photo_views, 
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
  r"quizs",
  matching_views.RoommateQuizViewSet,
  basename="quiz"
)

urlpatterns = [
  # internal admin actions
  path(
    "internal/profiles/", 
    internal_profiles.list_profiles, 
    name="list_profiles"
  ),
  path(
    "internal/profiles/delete/<pk>/",
    internal_profiles.delete_profile,
    name="delete_profile"
  ),
  path(
    "internal/profiles/fake/",
    internal_profiles.fake_create_profiles,
    name="create_fake_profiles"
  ),

  # authentication
  path(
    "token/refresh/", 
    TokenRefreshView.as_view(), 
    name="token_refresh"
  ),
  path(
    "users/login/",
    tokens.MyTokenObtainPairView.as_view(),
    name="login",
  ),

  # viewSets
  path("", include(router.urls)),
]