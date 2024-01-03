from rest_framework import viewsets, status
from rest_framework import serializers
from rest_framework.response import Response
from loopapi.models import Reaction


class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = ["id", "label"]


class reactionViewSet(viewsets.ViewSet):
    def list(self, request):
        Reactions = Reaction.objects.all()
        serializer = ReactionSerializer(Reactions, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            reaction = Reaction.objects.get(pk=pk)
            serializer = ReactionSerializer(reaction)
            return Response(serializer.data)
        except Reaction.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        # Get the data from the client's JSON payload
        label = request.data.get("label")

 
        # Create a comment database row first, so you have a
        # primary key to work with
        reaction = Reaction.objects.create(
            # maybe issues with label /  request.user
            label=label,
        )

        serializer = ReactionSerializer(reaction, context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        try:
            reaction = Reaction.objects.get(pk=pk)

            # Is the authenticated user allowed to edit this reaction?
            self.check_object_permissions(request, reaction)

            serializer = ReactionSerializer(data=request.data)
            if serializer.is_valid():
                reaction.label = serializer.validated_data["label"]
                # reaction.created_on = serializer.validated_data["created_on"]
                reaction.save()

                serializer = ReactionSerializer(reaction, context={"request": request})
                return Response(None, status.HTTP_204_NO_CONTENT)

            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        except Reaction.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            reaction = Reaction.objects.get(pk=pk)
            self.check_object_permissions(request, reaction)
            reaction.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except Reaction.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
