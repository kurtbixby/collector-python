# from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from api.models import Game, Platform

class GameAPITests(APITestCase):
    '''
    Class containing tests of the Version API endpoint
    '''
    # def setUp(self):
    #     platform = Platform.objects.create(platform_name='NX', manufacturer='Nintendo')
    #     self.assertEqual(platform.pk, 1)

    def test_game_post_creation(self):
        # url = reverse()
        game_json = {
            'game_name': 'Dragon Quest XI S',
            'versions': [
                {
                    'platform': {
                        'platform_name': 'NX',
                        'manufacturer': 'Nintendo',
                    },
                    'version_name': 'DQXIS',
                },
            ]
        }
        response = self.client.post('/api/game/', game_json, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class VersionAPITests(APITestCase):
    '''
    Class containing tests of the Version API endpoint
    '''
    def setUp(self):
        game = Game.objects.create(game_name='Dragon Quest XI')
        self.assertEqual(game.pk, 1)

    def test_version_post_creation_full(self):
        # url = reverse()
        version_json = {
            'platform': {
                'platform_name': 'NX',
                'manufacturer': 'Nintendo',
            },
            'version_name': 'DQXIS',
            'game_id': 1,
        }
        response = self.client.post('/api/version/', version_json, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # def test_version_post_creation_platform_id(self):
    #     # url = reverse()
    #     version_json = {
    #         'platform_id': 1,
    #         'version_name': 'DQXIS',
    #         'game_id': 1,
    #     }
    #     response = self.client.post('/api/version/', version_json, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)