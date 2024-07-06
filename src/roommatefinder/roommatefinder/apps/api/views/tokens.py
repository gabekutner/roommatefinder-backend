from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny

from ..serializers import profile_serializers


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
  def validate(self, attrs):
    data = super().validate(attrs)
    serializer = profile_serializers.ProfileSerializer(self.user).data
    for key, value in serializer.items():
      data[key] = value
    return data

class MyTokenObtainPairView(TokenObtainPairView):
  serializer_class = MyTokenObtainPairSerializer
  permission_classes = [AllowAny]