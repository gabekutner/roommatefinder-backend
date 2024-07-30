from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

class CustomUserManagerTestCase(TestCase):
    
  def setUp(self):
    self.UserModel = get_user_model()
    self.manager = self.UserModel.objects

  def test_create_user(self):
    """Test creating a user with valid credentials."""
    user = self.manager.create_user(
      identifier='testuser@example.com',
      password='password123',
      otp_verified=True,
    )
    self.assertEqual(user.identifier, 'testuser@example.com')
    self.assertTrue(user.check_password('password123'))
    self.assertTrue(user.is_active)
    self.assertFalse(user.is_superuser)
    self.assertFalse(user.is_staff)

  def test_create_superuser(self):
    """Test creating a superuser with valid credentials."""
    superuser = self.manager.create_superuser(
      identifier='admin@example.com',
      password='password123',
      otp_verified=True
    )
    self.assertEqual(superuser.identifier, 'admin@example.com')
    self.assertTrue(superuser.check_password('password123'))
    self.assertTrue(superuser.is_active)
    self.assertTrue(superuser.is_superuser)
    self.assertTrue(superuser.is_staff)

  def test_create_user_without_identifier(self):
    """ Test that creating a user without an identifier raises a ValueError. """
    with self.assertRaises(ValueError):
      self.manager.create_user(
        identifier='',
        password='password123',
        otp_verified=True
      )

  def test_create_superuser_with_missing_permissions(self):
    """ Test that creating a superuser without the required permissions raises a ValueError. """
    with self.assertRaises(ValueError):
      self.manager.create_superuser(
        identifier='admin@example.com',
        password='password123',
        is_staff=False,
        is_superuser=False,
        otp_verified=True
      )