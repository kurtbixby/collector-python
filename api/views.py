from django.shortcuts import render

from rest_framework import viewsets

from api.game_models import Game, Version, Edition
from api.game_model_serializers import GameSerializer, VersionSerializer, EditionSerializer

# Create your views here.

class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

class VersionViewSet(viewsets.ModelViewSet):
    queryset = Version.objects.all()
    serializer_class = VersionSerializer

class EditionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Edition.objects.all()
    serializer_class = EditionSerializer