from api.game_models import Game, Platform, Region, Company, Version, Country, Piece, Edition
from rest_framework import serializers

class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = ['id', 'platform_name', 'manufacturer']

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
    version_id = serializers.IntegerField(required=False)
    country = CountrySerializer()
    pieces = PieceSerializer(many=True)

    class Meta:
        model = Edition
        fields = ['id', 'version_id', 'edition_name', 'country', 'pieces']

    def create(self, validated_data):
        if 'version_id' not in validated_data:
            raise serializers.ValidationError('No version specified for new version')
        edition = ModelObjectCreator.create_edition(validated_data)

        return edition

class VersionSerializer(serializers.ModelSerializer):
    game_id = serializers.IntegerField(required=False)
    editions = EditionSerializer(many=True, required=False)
    platform = PlatformSerializer()
    region = RegionSerializer(required=False)
    publisher = CompanySerializer(required=False)
    developer = CompanySerializer(required=False)

    class Meta:
        model = Version
        fields = ['id', 'game_id', 'platform', 'version_name', 'region', 'release_date', 'publisher', 'developer', 'editions']

    def create(self, validated_data):
        if 'game_id' not in validated_data:
            raise serializers.ValidationError('No game specified for new version')
        version = ModelObjectCreator.create_version(validated_data)

        return version

class GameSerializer(serializers.ModelSerializer):
    versions = VersionSerializer(many=True, required=False)

    class Meta:
        model = Game
        fields = ['id', 'game_name', 'aliases', 'versions']
    
    def create(self, validated_data):
        game = ModelObjectCreator.create_game(validated_data)

        return game
        
class ModelObjectCreator():
    @staticmethod
    def get_or_create_base_model_object(model_name, validated_data):
        return globals()[model_name].objects.get_or_create(**validated_data)[0]

    @staticmethod
    def get_or_create_platform(validated_data):
        return Platform.objects.get_or_create(**validated_data)[0]

    @staticmethod
    def get_or_create_region(validated_data):
        return Region.objects.get_or_create(**validated_data)[0]

    @staticmethod
    def get_or_create_company(validated_data):
        return Company.objects.get_or_create(**validated_data)[0]

    @staticmethod
    def get_or_create_country(validated_data):
        return Country.objects.get_or_create(**validated_data)[0]
    
    @staticmethod
    def get_or_create_piece(validated_data):
        return Piece.objects.get_or_create(**validated_data)[0]
    
    @staticmethod
    def create_edition(validated_data):
        if 'country' in validated_data:
            validated_data['country'] = ModelObjectCreator.get_or_create_country(validated_data.pop['country'])
        piece_array_data = validated_data.pop['pieces'] if 'pieces' in validated_data else []

        edition = Edition.objects.create(**validated_data)
        for piece_data in piece_array_data:
            piece = ModelObjectCreator.get_or_create_piece(**piece_data)
            edition.pieces.add(piece)
        
        return edition

    @staticmethod
    def create_version(validated_data):
        if 'platform' in validated_data:
            validated_data['platform'] = ModelObjectCreator.get_or_create_platform(validated_data['platform'])
        if 'region' in validated_data:
            validated_data['region'] = ModelObjectCreator.get_or_create_region(validated_data['region'])
        if 'publisher' in validated_data:
            validated_data['publisher'] = ModelObjectCreator.get_or_create_company(validated_data['publisher'])
        if 'developer' in validated_data:
            validated_data['developer'] = ModelObjectCreator.get_or_create_company(validated_data['developer'])
        
        edition_array_data = validated_data.pop['editions'] if 'editions' in validated_data else []

        version = Version.objects.create(**validated_data)
        for edition_data in edition_array_data:
            edition_data['version'] = version
            ModelObjectCreator.create_edition(edition_data)
        
        return version

    @staticmethod
    def create_game(validated_data):
        version_array_data = validated_data.pop['versions'] if 'versions' in validated_data else []

        game = Game.objects.create(**validated_data)
        for version_data in version_array_data:
            version_data['game'] = game
            ModelObjectCreator.create_version(version_data)
