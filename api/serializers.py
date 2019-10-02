from api.game_models import Game, Platform, Region, Company, Version, Country, Piece, Edition
from rest_framework import serializers

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['id']

class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = ['platform_name']

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['region_code']

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['company_name']
        
class VersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Version
        fields = ['game', 'platform', 'version_name', 'region', 'release_date', 'publisher', 'developer']
        
class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        
class PieceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Piece

class EditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Edition
        