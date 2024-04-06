""" roommatefinder/apps/api/urls.py """
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

from .views import profile_views
from .internal import internal_profiles


router = routers.DefaultRouter()

router.register(
  r"profiles",
  profile_views.ProfileViewSet,
  basename="profile",
)

router.register(
  r"photos",
  profile_views.PhotoViewSet,
  basename="photo",
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
    profile_views.MyTokenObtainPairView.as_view(),
    name="login",
  ),

  # ModelViewSets
  path("", include(router.urls)),
]