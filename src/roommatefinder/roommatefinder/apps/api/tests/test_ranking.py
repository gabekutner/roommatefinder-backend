# -*- coding: utf-8 -*-
from django.test import TestCase
from roommatefinder.apps.api import models


class TestRanking(TestCase):
  """
  Test case for ranking profiles.
  
  This test case evaluates the ranking functionality of the `rank_profiles`
  method in the `Profile` model.
  """
  def setUp(self):
    self.user = models.Profile.objects.create(
      identifier="example@gmail.com", 
      is_superuser=False, 
      otp_verified=True,
      has_account=True,
      dorm_building="4",
      interests=["1", "2", "3"],
      major="Computer Engineering",
      state="CA"
    )

  def test_ranking_dorm_var(self):
    """
    Test the ranking of profiles based on dorm building variability.
    
    This test creates two additional profiles and ranks them relative to the 
    `self.user` profile based on the dorm building. It verifies that the profile
    with a matching dorm building (`"4"`) is ranked higher than the profile with
    a different dorm building (`"6"`).
    """
    models.Profile.objects.create(
      identifier="first", 
      is_superuser=False, 
      otp_verified=True,
      has_account=True,
      dorm_building="4", # variable
      interests=["1", "2" "3"],
      major="Computer Engineering",
      state="FL"
    )
    models.Profile.objects.create(
      identifier="second", 
      is_superuser=False, 
      otp_verified=True,
      has_account=True,
      dorm_building="6", # variable
      interests=["1", "2", "3"],
      major="Computer Engineering",
      state="FL"
    )
    # Get ranked profiles
    ranked_profiles = models.Profile.objects.rank_profiles(self.user)
    self.assertEqual(ranked_profiles[0].identifier, "first")


  def test_ranking_interests_var(self):
    """
    Test the ranking of profiles based on interests variability.
    
    This test creates two additional profiles and ranks them relative to the 
    `self.user` profile based on their interests. It verifies that the profile
    with more similar interests is ranked higher than the profile with less 
    similar interests.
    """
    models.Profile.objects.create(
      identifier="first", 
      is_superuser=False, 
      otp_verified=True,
      has_account=True,
      dorm_building="4", 
      interests=["1", "2", "3"], # variable
      major="Computer Engineering",
      state="FL"
    )
    models.Profile.objects.create(
      identifier="second", 
      is_superuser=False, 
      otp_verified=True,
      has_account=True,
      dorm_building="4", 
      interests=["1", "2"], # variable
      major="Computer Engineering",
      state="FL"
    )
    # Get ranked profiles
    ranked_profiles = models.Profile.objects.rank_profiles(self.user)
    self.assertEqual(ranked_profiles[0].identifier, "first")


  def test_ranking_major_variability(self):
    """
    Test the ranking of profiles based on major variability.
    
    This test creates two additional profiles and ranks them relative to the 
    `self.user` profile based on their majors. It verifies that the profile
    with the similar major is ranked higher than the profile with a different
    major.
    """
    models.Profile.objects.create(
      identifier="first", 
      is_superuser=False, 
      otp_verified=True,
      has_account=True,
      dorm_building="4", 
      interests=["1", "2", "3"], # variable
      major="Computer Engineering",
      state="FL"
    )
    models.Profile.objects.create(
      identifier="second", 
      is_superuser=False, 
      otp_verified=True,
      has_account=True,
      dorm_building="4", 
      interests=["1", "2", "3"], # variable
      major="Business",
      state="FL"
    )
    # Get ranked profiles
    ranked_profiles = models.Profile.objects.rank_profiles(self.user)
    self.assertEqual(ranked_profiles[0].identifier, "first")
  

  def test_ranking_state_variability(self):
    """
    Test the ranking of profiles based on state variability.
    
    This test creates two additional profiles and ranks them relative to the 
    `self.user` profile based on their states. It verifies that the profile
    with the a different state is ranked higher than the profile with the same
    state.
    """
    models.Profile.objects.create(
      identifier="first", 
      is_superuser=False, 
      otp_verified=True,
      has_account=True,
      dorm_building="4", 
      interests=["1", "2", "3"], # variable
      major="Computer Engineering",
      state="FL"
    )
    models.Profile.objects.create(
      identifier="second", 
      is_superuser=False, 
      otp_verified=True,
      has_account=True,
      dorm_building="4",
      interests=["1", "2", "3"],
      major="Computer Engineering",
      state="CA"
    )
    # Get ranked profiles
    ranked_profiles = models.Profile.objects.rank_profiles(self.user)
    self.assertEqual(ranked_profiles[0].identifier, "first")