from rest_framework import status
from rest_framework.response import Response


def only_admin_and_user(id, request):
   # only the current user and an admin can execute this function
  if id != request.user.id and not request.user.is_superuser:
    return Response(
      {"detail": "Not authorized.",},
      status=status.HTTP_401_UNAUTHORIZED,
    )