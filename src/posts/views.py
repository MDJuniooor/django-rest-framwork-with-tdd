from django.contrib.auth.models import User

from rest_framework import viewsets
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope

from posts.serializers import UserSerialzer

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [TokenHasReadWriteScope]
    serializer_class = UserSerialzer
    queryset = User.objects.all()
    
