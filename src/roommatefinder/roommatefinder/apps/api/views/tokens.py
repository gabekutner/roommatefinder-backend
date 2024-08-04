# -*- coding: utf-8 -*-
from typing import Dict, Any

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny

from ..serializers import profile_serializers


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
  """
  Custom serializer for obtaining JWT tokens with additional user profile data.

  Inherits from:
    TokenObtainPairSerializer (rest_framework_simplejwt)

  Methods:
    validate(attrs):
      Validates the user credentials and includes additional user profile data in the response.
  """
  def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Override the validate method to add user profile data to the token response.

    Parameters:
      attrs (dict): The user credentials (identifier and password).

    Returns:
      dict: The JWT token data combined with the serialized user profile data.
    """
    # Call the parent class's validate method to get the default token data
    data = super().validate(attrs)
    # Serialize the user profile data
    serializer = profile_serializers.BaseProfileSerializer(self.user).data
    # Add the serialized profile data to the token response
    for key, value in serializer.items():
      data[key] = value

    return data


class MyTokenObtainPairView(TokenObtainPairView):
  """
  Custom view for obtaining JWT tokens using the custom serializer.

  Inherits from:
    TokenObtainPairView (rest_framework_simplejwt)

  Attributes:
    serializer_class (Type[MyTokenObtainPairSerializer]): The custom serializer class to be used.
    permission_classes (list): List of permission classes for access control.
  """
  serializer_class = MyTokenObtainPairSerializer
  # Allows unrestricted access to the token endpoint.
  permission_classes = [AllowAny]