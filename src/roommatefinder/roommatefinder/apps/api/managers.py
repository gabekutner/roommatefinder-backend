# -*- coding: utf-8 -*-
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.db.models.functions import Coalesce
from django.db.models import Case, When, IntegerField, Value, Q

from roommatefinder.apps.api import models


class CustomUserManager(BaseUserManager):
  """
  Custom manager for the User model.
  
  This class manages the creation of user and superuser profiles. It includes
  methods for creating both regular users and superusers with appropriate
  attributes and validations.

  Methods:
    create_user(identifier, password, **extra_fields):
      Creates and saves a regular user profile with the specified identifier and password.
    
    create_superuser(identifier, password, **extra_fields):
      Creates and saves a superuser profile with the specified identifier and password.
    
    rank_profiles(user_profile):
      Ranks profiles based on dorm, common interests, shared major, and state.
  """
  def create_user(self, identifier: str, password: str, **extra_fields):
    """
    Create and save a regular user profile with the given identifier and password.
    
    Parameters:
      identifier (str): The unique identifier for the user (e.g., email address).
      password (str): The password for the user.
      **extra_fields: Additional fields to set on the user profile.

    Raises:
      ValueError: If the identifier is not provided.

    Returns:
      Profile: The created user profile instance.
    """
    if not identifier:
      raise ValueError(_("The Identifier must be set."))
    user = self.model(identifier=identifier, **extra_fields)
    user.set_password(password)
    user.save()
    return user
  

  def create_superuser(self, identifier: str, password: str, **extra_fields):
    """
    Create and save a superuser profile with the given identifier and password.
    
    Superusers have special permissions and must have `is_staff` and `is_superuser`
    attributes set to True.

    Parameters:
      identifier (str): The unique identifier for the superuser (e.g., email address).
      password (str): The password for the superuser.
      **extra_fields: Additional fields to set on the superuser profile.

    Raises:
      ValueError: If `is_staff` or `is_superuser` is not set to True.

    Returns:
      Profile: The created superuser profile instance.
    """
    extra_fields.setdefault("is_staff", True)
    extra_fields.setdefault("is_superuser", True)
    extra_fields.setdefault("is_active", True)

    if extra_fields.get("is_staff") is not True:
      raise ValueError(_("Superuser must have is_staff=True."))
    if extra_fields.get("is_superuser") is not True:
      raise ValueError(_("Superuser must have is_superuser=True."))
    return self.create_user(identifier, password, **extra_fields)
  

  def rank_profiles(self, user_profile):
    """
    Rank profiles based on dorm, common interests, shared major, and state.

    Parameters:
      user_profile (Profile): The profile of the current user to compare against.

    Returns:
      QuerySet: Profiles ordered by similarity score.
    """
    # Convert the user's interests to a set for easier comparison
    user_interests = set(user_profile.interests)
    # Base queryset, exclude current user
    profiles = self.get_queryset().exclude(id=user_profile.id)
    # Only get accounts with an account set up
    profiles = profiles.filter(has_account=True)
    # Get connections involving the user
    connections = models.Connection.objects.filter(
        Q(sender=user_profile.id) | Q(receiver=user_profile.id),
        accepted=True
    )
    # Remove connections from the results
    excluded_ids = connections.values_list('sender', 'receiver')
    excluded_ids = set(id for sublist in excluded_ids for id in sublist)
    
    # Exclude current user and their connections
    if not excluded_ids:
      excluded_ids = {user_profile.id}
    profiles = profiles.exclude(id__in=excluded_ids)

    # Annotate similarity scores
    profiles = profiles.annotate(
      # Dorm Building Match
      dorm_match=Coalesce(Case(
        When(dorm_building=user_profile.dorm_building, then=Value(1)),
        default=Value(0),
        output_field=IntegerField()
      ), 0),
      # Shared Major
      major_match=Coalesce(Case(
        When(major=user_profile.major, then=Value(1)),
        default=Value(0),
        output_field=IntegerField()
      ), 0),
     # Promote profiles from different states
      state_promotion=Case(
        When(state=user_profile.state, then=Value(0)),
        default=Value(1),
        output_field=IntegerField()
      )
    )
    # Execute the query to get all profiles
    profiles_list = list(profiles)
     # Calculate the common interests
    for profile in profiles_list:
      profile_common_interests = set(profile.interests)
      common_interests_count = len(user_interests & profile_common_interests)
      profile.common_interests = common_interests_count

    # Sort profiles based on the custom criteria
    sorted_profiles = sorted(
      profiles_list,
      key=lambda p: (p.dorm_match, p.common_interests, p.major_match, p.state_promotion),
      reverse=True
    )

    return sorted_profiles