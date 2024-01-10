from rest_framework import viewsets, status
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import permissions
from loopapi.models import Game, Platform

class IsGameCreator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Assuming 'user' is the ForeignKey to the User model in your Game model
        return obj.user == request.user


class GameSerializer(serializers.ModelSerializer):
  class Meta:
    model = Game
    fields = ["id", "title", "platform", "game_image_url"]

class GameViewSet(viewsets.ViewSet):
  permission_classes = [permissions.IsAuthenticated, IsGameCreator]
  def list(self, request):
    games = Game.objects.all()
    serializer = GameSerializer(games, many=True)
    return Response(serializer.data)
  
  def retrieve(self, request, pk=None):
    try:
      game = Game.objects.get(pk=pk)
      serializer = GameSerializer(game)
      return Response(serializer.data)
    except Game.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)
    
  def get_games_by_platform_id(platform_id):
    games = Game.objects.filter(platform_id=platform_id)
    return games
      
  def create(self, request):
        title = request.data.get("title")
        game_image_url = request.data.get("game_image_url")
        platform_id = request.data.get("platform")

        try:
            platform = Platform.objects.get(pk=platform_id)
        except Platform.DoesNotExist:
            return Response({"error": "Platform does not exist"}, status=status.HTTP_404_NOT_FOUND)

        # Associate the logged-in user as the creator of the game
        game = Game.objects.create(
            title=title,
            game_image_url=game_image_url,
            platform=platform,
            user=request.user
        )

        serializer = GameSerializer(game, context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

  
  def update(self, request, pk=None):
        try:
            game = Game.objects.get(pk=pk)

            # Ensure the request.user is the creator of the game
            self.check_object_permissions(request, game)

            serializer = GameSerializer(game, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Game.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

  def destroy(self, request, pk=None):
        try:
            game = Game.objects.get(pk=pk)
            self.check_object_permissions(request, game)
            game.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except Game.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)