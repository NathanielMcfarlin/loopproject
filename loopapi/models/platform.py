from django.db import models

class Platform(models.Model):
  """Database model for tracking events"""

  platform = models.CharField(max_length=100)
  platform_image = models.URLField()