from django.db import models


class PostReaction(models.Model):
  """Database model for tracking events"""

  reaction_id = models.ForeignKey("Reaction", on_delete=models.CASCADE, related_name="postReaction")
  post_id = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="postReaction")