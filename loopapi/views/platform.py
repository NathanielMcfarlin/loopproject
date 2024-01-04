from rest_framework import viewsets, status
from rest_framework import serializers
from rest_framework.response import Response
from loopapi.models import Platform

class PlatformSerializer(serializers.ModelSerializer):
  class Meta:
    model = Platform
    fields = ["id", "platform", "platform_image"]

class PlatformViewSet(viewsets.ViewSet):
  def list(self, request):
    platforms = Platform.objects.all()
    serializer = PlatformSerializer(platforms, many=True)
    return Response(serializer.data)
  
  def retrieve(self, request, pk=None):
    try:
      platform = Platform.objects.get(pk=pk)
      serializer = PlatformSerializer(platform)
      return Response(serializer.data)
    except Platform.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)
    
  def create(self, request):
    platform = request.data.get("platform")
    platform_image = request.data.get("platform_image")

    platform = Platform.objects.create(
      platform=platform,
      platform_image=platform_image
    )

    serializer = PlatformSerializer(platform, context={"request": request})
    return Response(serializer.data, status=status.HTTP_201_CREATED)
  
  def update(self, request, pk=None):
        try:
            platform = Platform.objects.get(pk=pk)

            # Is the authenticated user allowed to edit this platform?
            self.check_object_permissions(request, platform)

            serializer = PlatformSerializer(data=request.data)
            if serializer.is_valid():
                platform.platform = serializer.validated_data["platform"]
                platform.platform_image = serializer.validated_data["platform_image"]
                platform.save()

                serializer = PlatformSerializer(platform, context={"request": request})
                return Response(None, status.HTTP_204_NO_CONTENT)

            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        except Platform.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

  def destroy(self, request, pk=None):
        try:
            platform = Platform.objects.get(pk=pk)
            self.check_object_permissions(request, platform)
            platform.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except Platform.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)