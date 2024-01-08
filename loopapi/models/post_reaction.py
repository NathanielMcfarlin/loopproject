from django.db import models
from django.contrib.auth.models import User


class PlatformPostReaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="platform_post_reactions")
    post = models.ForeignKey("PlatformPost", on_delete=models.CASCADE, related_name="platform_post_reactions")
    reaction = models.ForeignKey("Reaction", on_delete=models.CASCADE, related_name="platform_post_reactions")
    # other fields as needed

class GamePostReaction(models.Model):
    post = models.ForeignKey("GamePost", on_delete=models.CASCADE, related_name="game_reactions")
    reaction = models.ForeignKey("Reaction", on_delete=models.CASCADE, related_name="game_post_reactions")
    # other fields as needed
