from rest_framework import serializers
from rest_framework.test import APITestCase
from rest_framework.exceptions import ValidationError
from roommatefinder.apps.api.utils.model_utils import ChoicesField
from model_utils import Choices


class TestChoicesField(APITestCase):
  def setUp(self):
    self.choices = Choices(
      ("A", "Choice A"), 
      ("B", "Choice B"),
      ("C", "Choice C")
    )

    class TestSerializer(serializers.Serializer):
      status = ChoicesField(choices=self.choices)
      
    self.serializer_class = TestSerializer

  def test_to_representation(self):
    # Test converting internal value to human-readable form
    instance = {'status': 'A'}  # This is the internal value
    serializer = self.serializer_class(instance=instance)
    data = serializer.data
    # Check if 'A' is converted to 'Choice A'
    self.assertEqual(data['status'], 'Choice A')

  def test_to_internal_value(self):
    # Test converting human-readable value to internal value
    data = {'status': 'Choice A'}  # This is the human-readable form
    serializer = self.serializer_class(data=data)
    
    # self.assertTrue(serializer.is_valid())
    # Validate that 'Choice A' is converted to 'A'
    # self.assertEqual(serializer.validated_data['status'], 'A')

  def test_invalid_to_internal_value(self):
    # Test if invalid values raise a validation error
    data = {'status': 'Invalid Choice'}
    serializer = self.serializer_class(data=data)
    with self.assertRaises(ValidationError):
      serializer.is_valid(raise_exception=True)