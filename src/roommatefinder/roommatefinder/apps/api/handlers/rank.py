""" roommatefinder/apps/api/handlers/swipe_filters.py """
from django.db.models import Case, When


def rank_profiles(current_profile, profiles):
  """ ranking algorithm 

  1. by dorm
  2. by major
  """
  user_sex = current_profile.sex
  user_dorm = current_profile.dorm_building
  user_major = current_profile.major

  blocked_profiles = current_profile.blocked_profiles.all()

  # by sex and blocked profiles
  show_profiles = profiles.filter(sex=user_sex).exclude(id__in=blocked_profiles)


  dorms_at_top = [user_dorm]
  majors_at_top = [user_major]

  show_profiles = show_profiles.order_by(Case(
    When(dorm_building__in=dorms_at_top, then=0),
    When(major__in=majors_at_top, then=1)
    )
  )
  
  return show_profiles