# from django.test import TestCase
# from django.urls import reverse
# from rest_framework.test import APIClient
# from rest_framework import status
# from loopapi.models import Game, Platform
# from loopapi.views.game import GameSerializer


# class GameTest(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.platform = Platform.objects.create(platform="Test Platform", platform_image="http://example.com/test_image.jpg")
#         self.game = Game.objects.create(
#             title="Test Game",
#             platform=self.platform,
#             game_image_url="http://example.com/test_game_image.jpg"
#         )

#     def test_list_games(self):
#         url = reverse("game-list")
#         response = self.client.get(url)
#         games = Game.objects.all()
#         serializer = GameSerializer(games, many=True)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data, serializer.data)

#     def test_retrieve_game(self):
#         url = reverse("game-detail", args=[self.game.id])
#         response = self.client.get(url)
#         serializer = GameSerializer(self.game)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data, serializer.data)

#     def test_create_game(self):
#         url = reverse("game-list")
#         data = {
#             "title": "New Test Game",
#             "platform": self.platform.id,
#             "game_image_url": "http://example.com/new_test_game_image.jpg"
#         }
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(Game.objects.count(), 2)

#     def test_update_game(self):
#         url = reverse("game-detail", args=[self.game.id])
#         updated_data = {
#             "title": "Updated Test Game",
#             "game_image_url": "http://example.com/updated_test_game_image.jpg"
#         }
#         response = self.client.put(url, updated_data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.game.refresh_from_db()
#         self.assertEqual(self.game.title, updated_data["title"])
#         self.assertEqual(self.game.game_image_url, updated_data["game_image_url"])

#     def test_delete_game(self):
#         url = reverse("game-detail", args=[self.game.id])
#         response = self.client.delete(url)
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertEqual(Game.objects.count(), 0)
