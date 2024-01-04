from django.db import models
from django.contrib.auth.models import User

class PlatformPost(models.Model):
    """Database model for tracking events"""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="platform_posts")
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    post_image_url = models.URLField()
    link = models.URLField()
    timestamp = models.DateField(auto_now_add=True)
    platform = models.ForeignKey("Platform", on_delete=models.CASCADE, related_name="platform_posts")
    is_staff = models.BooleanField()
    reactions = models.ManyToManyField("Reaction", through="PlatformPostReaction", related_name="platform_posts")


class GamePost(models.Model):
    """Database model for tracking events"""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="game_posts")
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    post_image_url = models.URLField()
    link = models.URLField()
    timestamp = models.DateField(auto_now_add=True)
    game = models.ForeignKey("Game", on_delete=models.CASCADE, related_name="game_posts")
    is_staff = models.BooleanField()
    reactions = models.ManyToManyField("Reaction", through="GamePostReaction", related_name="game_posts")
