from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import serializers
from loopapi.models import PlatformPost, GamePost, Game, Platform, Reaction
from django.contrib.auth.models import User
from .reaction import ReactionSerializer
from .platform import PlatformSerializer
from .game import GameSerializer
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
import json


class PlatformPostSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    is_staff = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    # reactions = ReactionSerializer(many=True, read_only=True)
    platform = PlatformSerializer(many=False, read_only=True)
    liked = serializers.SerializerMethodField()

    
    def get_is_staff(self, obj):
        # Check if the authenticated user is the owner
        return self.context["request"].user == obj.user
    
    def get_is_owner(self, obj):
        return self.context["request"].user == obj.user
    
    def get_liked(self, obj):
        msg = False
    
        if self.context["request"].user:
            user = self.context["request"].user
    
        if  obj.likes.filter(id=user.id).exists():
            msg = True

        return msg

    class Meta:
        model = PlatformPost
    
        fields = [
            "id",
            "title",
            "description",
            "post_image_url",
            "link",
            "timestamp",
            "platform",
            "user",
            "likes",
            "is_staff",
            "is_owner",
            "liked"
        ]

class UpdatePlatformPostSerializer(serializers.ModelSerializer):
    platform = PlatformSerializer(many=False, read_only=True)


    class Meta:
        model = PlatformPost
    
        fields = [
            "title",
            "description",
            "post_image_url",
            "link",
            "platform",
        ]


class PlatformPostViewSet(viewsets.ViewSet):
    def list(self, request):
        posts = PlatformPost.objects.all()
        serializer = PlatformPostSerializer(posts, many=True, context={"request": request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            post = PlatformPost.objects.get(pk=pk)
            serializer = PlatformPostSerializer(post, context={"request": request})
            return Response(serializer.data)

        except PlatformPost.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        # Get the data from the client's JSON payload
        user = request.user
        # reaction_ids = Reaction.objects.get(pk=request.data["reactions"])
        platform_id = Platform.objects.get(pk=request.data["platform"])
        title = request.data.get("title")
        link = request.data.get("link")
        timestamp = request.data.get("timestamp")
        post_image_url = request.data.get("post_image_url")
        description = request.data.get("description")
        is_staff = request.data.get("is_staff")
        

        try:
            platform_id = request.data.get("platform")
        except Platform.DoesNotExist:
            return Response({"error": "Platform does not exist"}, status=status.HTTP_404_NOT_FOUND)
        # Create a post database row first, so you have a
        # primary key to work with
        platform = Platform.objects.get(pk=platform_id)
        post = PlatformPost.objects.create(
            # maybe issues with rare_user /  request.user
            user=user,
            title=title,
            link=link,
            timestamp=timestamp,
            post_image_url=post_image_url,
            platform=platform,
            description=description,
            is_staff=is_staff,
            
        )

        # Establish the many-to-many relationships
        # reactions_ids = request.data.get("reactions", [])
        # print("Reactions IDs extracted:", reactions_ids)
        # post.reactions.set(reactions_ids)

        serializer = PlatformPostSerializer(post, context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        try:
            post = PlatformPost.objects.get(pk=pk)
            serializer = UpdatePlatformPostSerializer(data=request.data)
            if serializer.is_valid():
                post.title = serializer.validated_data["title"]
                post.link = serializer.validated_data["link"]
                post.post_image_url = serializer.validated_data["post_image_url"]
                # post.timestamp = serializer.validated_data["timestamp"]
                # post.user = serializer.validated_data["user"]
                post.description = serializer.validated_data["description"]
                if request.data["platform"]:
                    platform = Platform.objects.get(pk=request.data["platform"])
                    post.platform = platform
                # post.is_staff = serializer.validated_data["is_staff"]
                post.save()

                
                serializer = PlatformPostSerializer(post, context={"request": request})
                return Response(None, status.HTTP_204_NO_CONTENT)

            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            post = PlatformPost.objects.get(pk=pk)
            self.check_object_permissions(request, post)
            post.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except PlatformPost.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    

#! ------------------------------------------End of platfrom post viewset--------------------------------------------------------------------------


class GamePostSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    is_staff = serializers.SerializerMethodField()
    reactions = ReactionSerializer(many=True)
    game = GameSerializer(many=False)
    
    def get_is_staff(self, obj):
        # Check if the authenticated user is the owner
        return self.context["request"].user == obj.user

    class Meta:
        model = GamePost
        fields = [
            "id",
            "title",
            "description",
            "post_image_url",
            "link",
            "timestamp",
            "game",
            "user",
            "reactions",
            "is_staff"
        ]

class GamePostViewSet(viewsets.ViewSet):
    def list(self, request):
        posts = GamePost.objects.all()
        serializer = GamePostSerializer(posts, many=True, context={"request": request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            post = GamePost.objects.get(pk=pk)
            serializer = GamePostSerializer(post, context={"request": request})
            return Response(serializer.data)

        except GamePost.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        # Get the data from the client's JSON payload
        user = request.user
        game_id = request.data.get("game")
        title = request.data.get("title")
        link = request.data.get("link")
        timestamp = request.data.get("timestamp")
        post_image_url = request.data.get("post_image_url")
        description = request.data.get("description")
        is_staff = request.data.get("is_staff")
        
        try:
            game = Game.objects.get(pk=game_id)
        except Game.DoesNotExist:
            return Response({"error": "Game does not exist"}, status=status.HTTP_404_NOT_FOUND)

        post = GamePost.objects.create(
            user=user,
            title=title,
            link=link,
            timestamp=timestamp,
            post_image_url=post_image_url,
            game=game,
            description=description,
            is_staff=is_staff,
        )

        reactions_ids = request.data.get("reactions", [])
        print("Reactions IDs extracted:", reactions_ids)
        post.reactions.set(reactions_ids)

        serializer = GamePostSerializer(post, context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    # def update(self, request, pk=None):
    #     try:
    #         post = GamePost.objects.get(pk=pk)

    #         # Is the authenticated user allowed to edit this post?
    #         self.check_object_permissions(request, post)

    #         serializer = SimplePostSerializer(data=request.data)
    #         if serializer.is_valid():
    #             # post.user = serializer.validated_data["user"]
    #             post.reactions = serializer.validated_data["reactions"]
    #             post.title = serializer.validated_data["title"]
    #             # post.timestamp = serializer.validated_data["timestamp"]
    #             post.post_image_url = serializer.validated_data["post_image_url"]
    #             post.description = serializer.validated_data["description"]
    #             post.approved = serializer.validated_data["approved"]
    #             post.save()

    #             tag_ids = request.data.get("tags", [])
    #             post.tags.set(tag_ids)

    #             serializer = PostSerializer(post, context={"request": request})
    #             return Response(None, status.HTTP_204_NO_CONTENT)

    #         return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    #     except GamePost.DoesNotExist:
    #         return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            post = GamePost.objects.get(pk=pk)
            self.check_object_permissions(request, post)
            post.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except GamePost.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
