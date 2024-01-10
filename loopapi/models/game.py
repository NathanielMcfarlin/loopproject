from django.db import models
from django.contrib.auth.models import User


class Game(models.Model):
  """Database model for tracking events"""

  title = models.CharField(max_length=100)
  platform = models.ForeignKey("Platform", on_delete=models.CASCADE, related_name="game")
  game_image_url = models.URLField(max_length=5000)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
