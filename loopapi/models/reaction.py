from django.db import models

class Reaction(models.Model):
  """Database model for tracking events"""

  label = models.CharField(max_length=50)
  