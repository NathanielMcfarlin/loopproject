from django.db import models


class PlatformPostReaction(models.Model):
    post = models.ForeignKey("PlatformPost", on_delete=models.CASCADE, related_name="platform_reactions")
    reaction = models.ForeignKey("Reaction", on_delete=models.CASCADE, related_name="platform_post_reactions")
    # other fields as needed

class GamePostReaction(models.Model):
    post = models.ForeignKey("GamePost", on_delete=models.CASCADE, related_name="game_reactions")
    reaction = models.ForeignKey("Reaction", on_delete=models.CASCADE, related_name="game_post_reactions")
    # other fields as needed
