from django.db import models


class Game(models.Model):
  """Database model for tracking events"""

  title = models.CharField(max_length=100)
  platformId = models.ForeignKey("Platform", on_delete=models.CASCADE, related_name="game")
  game_image_url = models.URLField()
