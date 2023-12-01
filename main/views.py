from rest_framework import viewsets
from rest_framework import permissions

from .serializers import *
from .models import *


class UserViewset(viewsets.ModelViewSet):
   queryset = User.objects.all()
   serializer_class = UserSerializer


class CoordsViewset(viewsets.ModelViewSet):
   queryset = Coords.objects.all()
   serializer_class = CoordsSerializer


class LevelViewset(viewsets.ModelViewSet):
   queryset = Level.objects.all()
   serializer_class = LevelSerializer


class PerevalViewest(viewsets.ModelViewSet):
   queryset = Pereval.objects.all()
   serializer_class = PerevalSerializer


class ImagesViewest(viewsets.ModelViewSet):
   queryset = Images.objects.all()
   serializer_class = ImagesSerializer
