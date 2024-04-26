""" roommatefinder/apps/api/views/reset_views.py """
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny



@api_view(["POST"])
@permission_classes([AllowAny])
def recovery_code(request):
  data = request.data
  email = data["email"]

  # need an email backend, do later