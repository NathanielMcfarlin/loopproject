from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import serializers
from rareapi.models import Post, RareUser, Category
from django.contrib.auth.models import User
from .tags import TagSerializer
from .users import RareUserSerializer
from .categories import CategorySerializer


# class SimplePostSerializer(serializers.ModelSerializer):
#     # is_owner = serializers.SerializerMethodField()

#     # def get_is_owner(self, obj):
#     #     # Check if the authenticated user is the owner
#     #     return self.context["request"].user == obj.user.user

#     class Meta:
#         model = Post
#         fields = [
#             "title",
#             "link",
#             "post_image_url",
#             "description",
#             "reactions",
#             "game",
#             "platform"
#             # "is_owner",
#         ]


class PostSerializer(serializers.ModelSerializer):
    user = RareUserSerializer(many=False)
    is_owner = serializers.SerializerMethodField()
    reactions = ReactionsSerializer(many=True)
    platform = PlatformSerializer(many=False)
    game = GameSerializer(many=False)
    
    def get_is_owner(self, obj):
        # Check if the authenticated user is the owner
        return self.context["request"].user == obj.user

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "description",
            "post_image_url",
            "link",
            "timestamp",
            "platform",
            "game",
            "user"
            "reactions",
            "is_owner",
        ]


class PostViewSet(viewsets.ViewSet):
    def list(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True, context={"request": request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            post = Post.objects.get(pk=pk)
            serializer = PostSerializer(post, context={"request": request})
            return Response(serializer.data)

        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        # Get the data from the client's JSON payload
        user = User.objects.get(user=request.auth.user)
        reaction_ids = Reactions.objects.get(pk=request.data["reactions"])
        game = Game.objects.get(pk=request.data["game"])
        platform = Platform.objects.get(pk=request.data["platform"])
        title = request.data.get("title")
        link = request.data.get("link")
        timestamp = request.data.get("timestamp")
        post_image_url = request.data.get("post_image_url")
        description = request.data.get("content")
        is_owner = request.data.get("is_owner")

        # Create a post database row first, so you have a
        # primary key to work with
        post = Post.objects.create(
            # maybe issues with rare_user /  request.user
            user=user,
            title=title,
            link=link,
            timestamp=timestamp,
            post_image_url=post_image_url,
            game=game,
            platform=platform,
            description=description,
            is_owner=is_owner,
        )

        # Establish the many-to-many relationships
        reaction_ids = request.data.get("reactions", [])
        post.reaction.set(reaction_ids)

        serializer = PostSerializer(post, context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # def update(self, request, pk=None):
    #     try:
    #         post = Post.objects.get(pk=pk)

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

    #     except Post.DoesNotExist:
    #         return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            post = Post.objects.get(pk=pk)
            self.check_object_permissions(request, post)
            post.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
