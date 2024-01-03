from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    """Database model for tracking events"""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    post_image_url = models.URLField()
    link = models.URLField()
    timestamp = models.DateField(auto_now_add=True)
    platform_id = models.ForeignKey("Platform", on_delete=models.CASCADE, related_name="posts")
    game_id = models.ForeignKey("Game", on_delete=models.CASCADE, related_name="posts")
