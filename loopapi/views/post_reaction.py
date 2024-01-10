from rest_framework import viewsets, status
from rest_framework import serializers
from rest_framework.response import Response
from loopapi.models import PlatformPostReaction
from loopapi.models import PlatformPost
from loopapi.models import Reaction
from django.core.exceptions import ObjectDoesNotExist


class PostReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlatformPostReaction
        fields = ["user", "post", "reaction"]


# class PostReactionViewSet(viewsets.ViewSet):


    # def create(self, request):
    #     # Get the data from the client's JSON payload
    #     postId = request.data.get("postId")
    #     reactionId = request.data.get("reactionId")
    #     post = PlatformPost.objects.get(pk=postId)
    #     reaction = Reaction.objects.get(pk=reactionId)
    #     try:
    #         post_reaction = PlatformPostReaction.objects.get(
    #             post=post,
    #             user=request.user
    #         )
    #     except ObjectDoesNotExist:
    #         post_reaction = PlatformPostReaction.objects.create(
    #             post=post,
    #             reaction=reaction,
    #             user=request.user
    #         )
    #         serializer = PostReactionSerializer(post_reaction, context={"request": request})
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     else: 
    #         if post_reaction.reaction.id == reactionId:
    #             post_reaction.delete()
    #             return Response(status=status.HTTP_204_NO_CONTENT)
    #         else: 
    #             post_reaction.reaction = reaction
    #             post_reaction.save()
    #             serializer = PostReactionSerializer(post_reaction, context={"request": request})
    #             return Response(serializer.data, status=status.HTTP_201_CREATED)


class PostReactionViewSet(viewsets.ViewSet):

    def create(self, request):
        postId = request.data.get("postId")
        reactionId = request.data.get("reactionId")
        post = PlatformPost.objects.get(pk=postId)
        reaction = Reaction.objects.get(pk=reactionId)

        try:
            post_reaction = PlatformPostReaction.objects.get(
                post=post,
                user=request.user
            )
        except ObjectDoesNotExist:
            post_reaction = PlatformPostReaction.objects.create(
                post=post,
                reaction=reaction,
                user=request.user
            )
            serializer = PostReactionSerializer(post_reaction, context={"request": request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            if post_reaction.reaction.id == reactionId:
                # Reaction exists and matches the new reaction ID
                return Response({"message": "Reaction already exists"}, status=status.HTTP_200_OK)
            else:
                # Update the existing reaction
                post_reaction.reaction = reaction
                post_reaction.save()
                serializer = PostReactionSerializer(post_reaction, context={"request": request})
                return Response(serializer.data, status=status.HTTP_200_OK)
