from django.db import models


class Post(models.Model):
  """Database model for tracking events"""

  user_id = models.ForeignKey("User", on_delete=models.CASCADE, related_name="post")
  title = models.CharField(max_length=200)
  description = models.CharField(max_length=1000)
  post_image_url = models.URLField()
  link = models.URLField()
  timestamp = publication_date = models.DateField(auto_now_add=True)
  platform_id = models.ForeignKey("Platform", on_delete=models.CASCADE, related_name="post")
  game_id = models.ForeignKey("Game", on_delete=models.CASCADE, related_name="post")