from loopapi.models import PlatformPost
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.http import  JsonResponse
from json.decoder import JSONDecodeError
import json


class LikesViewSet(viewsets.ViewSet):

  def retrieve(self, request, pk):
      post = PlatformPost.objects.get(pk = pk)
      msg = False
      
      if request.user:
          user = request.user
          
      
          if post.likes.filter(id=user.id).exists():
              msg = True
      
      return JsonResponse(request, {'post': post, 'msg':msg})


  def create(self, request):
      data = json.loads(request.body)
      id = data["id"]
      post = PlatformPost.objects.get(id=id)
      checker = None
      
      if request.user:
          
          if post.likes.filter(id=request.user.id).exists():
              post.likes.remove(request.user)
              checker = 0
              
              
          else:
              post.likes.add(request.user)
              checker = 1

      return Response({"check": checker})

