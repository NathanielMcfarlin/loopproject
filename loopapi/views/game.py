from rest_framework import viewsets, status
from rest_framework import serializers
from rest_framework.response import Response
from loopapi.models import Game, Platform

class GameSerializer(serializers.ModelSerializer):
  class Meta:
    model = Game
    fields = ["id", "title", "platform", "game_image_url"]

class GameViewSet(viewsets.ViewSet):
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
      platform_id = request.data.get("platform")  # Corrected variable name
      game_image_url = request.data.get("game_image_url")

      try:
          platform = Platform.objects.get(pk=platform_id)
      except Platform.DoesNotExist:
          return Response({"error": "Platform does not exist"}, status=status.HTTP_404_NOT_FOUND)

      game = Game.objects.create(
          title=title,
          game_image_url=game_image_url,
          platform=platform
      )

      serializer = GameSerializer(game, context={"request": request})
      return Response(serializer.data, status=status.HTTP_201_CREATED)

  
  def update(self, request, pk=None):
        try:
            game = Game.objects.get(pk=pk)

            # Is the authenticated user allowed to edit this game?
            self.check_object_permissions(request, game)

            serializer = GameSerializer(data=request.data)
            if serializer.is_valid():
                game.game = serializer.validated_data["game"]
                game.platform_image = serializer.validated_data["platform_image"]
                game.save()

                serializer = GameSerializer(game, context={"request": request})
                return Response(None, status.HTTP_204_NO_CONTENT)

            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

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