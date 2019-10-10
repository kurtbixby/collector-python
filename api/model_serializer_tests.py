from collections import OrderedDict

from django.test import TestCase

from .game_models import Game, Platform, Region, Company, Version, Country, Piece, Edition
from .serializers import GameSerializer, PlatformSerializer, RegionSerializer, CompanySerializer, VersionSerializer, CountrySerializer, PieceSerializer, EditionSerializer

# Create your tests here.
'''
class GameSerializerTests(TestCase):
    def test_full_serialization(self):
        game = Game()
        serializer = GameSerializer(instance=game)
        self.assertEqual(set(serializer.data.keys), )
'''

def test_flat_serialization(test_class, class_name, expected_fields):
    instance = globals()[class_name](**expected_fields)
    serializer = globals()[class_name+'Serializer'](instance=instance)
    actual_fields = serializer.data
    test_class.assertDictEqual(actual_fields, expected_fields)

def test_nested_serialization(test_class, class_name, instance, expected_fields):
    serializer = globals()[class_name+'Serializer'](instance=instance)
    actual_fields = serializer.data
    assertNestedModelEqual(test_class, dict(actual_fields), expected_fields)

def assertNestedModelEqual(test_class, model_dict, expected_dict):
    test_class.assertEqual(set(model_dict.keys()), set(expected_dict.keys()))
    for k in expected_dict.keys():
        if isinstance(model_dict[k], OrderedDict):
            assertNestedModelEqual(test_class, dict(model_dict[k]), expected_dict[k])
        elif isinstance(model_dict[k], list):
            for i in range(len(model_dict[k])):
                assertNestedModelEqual(test_class, model_dict[k][i], expected_dict[k][i])
        else:
            test_class.assertEqual(model_dict[k], expected_dict[k])
            
class PlatformSerializerTests(TestCase):
    class_name = 'Platform'

    def test_platform_flat_serialization(self):
        fields = {  'id': 1,
                    'platform_name': 'Nintendo Switch'}
        test_flat_serialization(self, class_name=self.class_name, expected_fields=fields)

class RegionSerializerTests(TestCase):
    class_name = 'Region'

    def test_region_flat_serialization(self):
        fields = {  'id': 1,
                    'region_code': 'NTSC-J'}
        test_flat_serialization(self, class_name=self.class_name, expected_fields=fields)

class CompanySerializerTests(TestCase):
    class_name = 'Company'

    def test_company_flat_serialization(self):
        fields = {  'id': 1,
                    'company_name':'Square-Enix'}
        test_flat_serialization(self, class_name=self.class_name, expected_fields=fields)

class CountrySerializerTests(TestCase):
    class_name = 'Country'

    def test_country_flat_serialization(self):
        fields = {  'id': 1,
                    'country_code': 'USA',
                    'country_name': 'United State of America',}
        test_flat_serialization(self, class_name=self.class_name, expected_fields=fields)

class PieceSerializerTests(TestCase):
    class_name = 'Piece'

    def test_piece_flat_serialization(self):
        fields = {  'id': 1,
                    'piece_type': 'Manual'}
        test_flat_serialization(self, class_name=self.class_name, expected_fields=fields)

class EditionSerializerTests(TestCase):
    class_name = 'Edition'

    def test_edition_serialization(self):
        game = Game.objects.create()
        version = Version.objects.create(
            platform=Platform.objects.create(platform_name='NX'),
            version_name='DQXIS',
            game=game
        )
        country = Country.objects.create(
            country_code='USA',
            country_name='United States of America')
        pieces = [
            Piece.objects.create(piece_type='Manual'),
            Piece.objects.create(piece_type='Stickers'),
        ]
        edition = Edition.objects.create(
            version=version,
            edition_name='Standard Edition',
            country = country,
        )
        for p in pieces:
            edition.pieces.add(p)

        fields = {
            'id': 1,
            'edition_name': 'Standard Edition',
            'country': {  'id': 1,
                    'country_code': 'USA',
                    'country_name': 'United States of America',
            },
            'pieces': [
                {  'id': 1,
                    'piece_type': 'Manual'},
                {  'id': 2,
                    'piece_type': 'Stickers'}
            ]
        }

        test_nested_serialization(self, class_name=self.class_name, instance=edition, expected_fields=fields)

class VersionSerializerTests(TestCase):
    class_name = 'Version'

    def test_version_serialization(self):
        game = Game.objects.create()
        instance = Version.objects.create(
            platform=Platform.objects.create(platform_name='NX'),
            version_name='DQXIS',
            game=game
        )

        fields = {
            'id': 1,
            'platform': {
                'id': 1,
                'platform_name': 'NX'
            },
            'version_name': 'DQXIS',
            'game': 1,
            'release_date': None,
            'editions': None,
            'developer': None,
            'publisher': None,
            'region': None,
        }

        test_nested_serialization(self, class_name=self.class_name, instance=instance, expected_fields=fields)

class GameSerializerTests(TestCase):
    class_name = 'Game'

    def test_edition_serialization(self):
        game = Game.objects.create()
        Version.objects.create(
            platform=Platform.objects.create(platform_name='NX'),
            version_name='DQXIS',
            game=game
        )
        Version.objects.create(
            platform=Platform.objects.create(platform_name='3DS'),
            version_name='DQXI',
            game=game
        )
        
        # fields = 

        fields = {
            'id': 1,
            'versions': [
                {
                    'id': 1,
                    'platform': {
                        'id': 1,
                        'platform_name': 'NX'
                    },
                    'version_name': 'DQXIS',
                    'game': 1,
                    'release_date': None,
                    'editions': None,
                    'developer': None,
                    'publisher': None,
                    'region': None,
                },
                {
                    'id': 2,
                    'platform': {
                        'id': 2,
                        'platform_name': '3DS'
                    },
                    'version_name': 'DQXI',
                    'game': 1,
                    'release_date': None,
                    'editions': None,
                    'developer': None,
                    'publisher': None,
                    'region': None,
                },
            ]
        }
        self.maxDiff = None
        test_nested_serialization(self, class_name=self.class_name, instance=game, expected_fields=fields)