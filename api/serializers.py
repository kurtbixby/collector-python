from api.game_models import Game, Platform, Region, Company, Version, Country, Piece, Edition
from rest_framework import serializers

class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = ['id', 'platform_name']

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'region_code']

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'company_name']

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'country_code', 'country_name']
        
class PieceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Piece
        fields = ['id', 'piece_type']

class EditionSerializer(serializers.ModelSerializer):
    country = CountrySerializer()
    pieces = PieceSerializer(many=True)

    class Meta:
        model = Edition
        fields = ['id', 'edition_name', 'country', 'pieces']

class VersionSerializer(serializers.ModelSerializer):
    editions = EditionSerializer(many=True)
    platform = PlatformSerializer()
    region = RegionSerializer()
    publisher = CompanySerializer()
    developer = CompanySerializer()

    class Meta:
        model = Version
        fields = ['id', 'game', 'platform', 'version_name', 'region', 'release_date', 'publisher', 'developer', 'editions']

class GameSerializer(serializers.ModelSerializer):
    versions = VersionSerializer(many=True)

    class Meta:
        model = Game
        fields = ['id', 'versions']
        