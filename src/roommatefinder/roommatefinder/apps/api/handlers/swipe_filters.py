from datetime import date
from django.utils.timezone import now


def age_range(data, min_age, max_age):
  current = now().date()
  min_date = date(current.year - min_age, current.month, current.day)
  max_date = date(current.year - max_age, current.month, current.day)

  return data.filter(birthdate__gte=max_date, birthdate__lte=min_date)


def filter_profiles(current_profile):
  """ algorithm function """
  profile_age = current_profile.age
  blocked_profiles = current_profile.blocked_profiles.all()

  # Exclude the blocked profiles the user has
  show_profiles = show_profiles.exclude(id__in=blocked_profiles)

  # Exclude any profile that has blocked the current user
  if current_profile.blocked_by.all().exists():
    blocked_by_profiles = current_profile.blocked_by.all()
    show_profiles = show_profiles.exclude(id__in=blocked_by_profiles)

  # Show profiles between in a range of ages
  if profile_age == 18 or profile_age == 19:
    show_profiles = age_range(show_profiles, profile_age - 1, profile_age + 6)
  else:
    show_profiles = age_range(show_profiles, profile_age - 5, profile_age + 5)

  # Exclude the current user in the swipe
  show_profiles = show_profiles.exclude(id=current_profile.id)

  return show_profiles