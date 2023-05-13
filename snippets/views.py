"""
from .models import Snippet
from .serializers import SnippetSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

Boring way:
# All snippets
class SnippetList(APIView):
    def get(self, request, format=None):
        # get all data
        snippets = Snippet.objects.all()
        # serialize the data
        serializer = SnippetSerializer(snippets, many=True)
        # retrieve the data
        return Response(serializer.data)

    def post(self, request, format=None):
        # deserialize the data
        serializer = SnippetSerializer(data=request.data)
        # data validation
        if serializer.is_valid():
            # data saving
            serializer.save()
            # confirmation message
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # error message
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# Specific snippet
class SnippetDetail(APIView):
    def get_object(self, pk):
        try:
            # trying to get the specific instance by its pk
            return Snippet.objects.get(pk=pk)
        except Snippet.DoesNotExist:
            # raising an error if such instance does not exist
            raise Http404
        
    def get(self, request, pk, format=None):
        # executing the previous function and storing the values
        snippet = self.get_object(pk)
        # serialize the data
        serializer = SnippetSerializer(snippet)
        # retrieve the data
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        # retrieving the old data
        snippet = self.get_object(pk)
        # serialize the provided data if it does exist, if not, use the old data
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            # data updating
            serializer.save()
            # confirmation message
            return Response(serializer.data)
        # error message
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        # retrieving the data
        snippet = self.get_object(pk)
        # removing the data
        snippet.delete()
        # confirmation message
        return Response(status=status.HTTP_204_NO_CONTENT)"""


"""
from .models import Snippet
from .serializers import SnippetSerializer
from rest_framework import mixins
from rest_framework import generics

Mixing way:
class SnippetList(
    mixins.ListModelMixin, 
    mixins.CreateModelMixin, 
    generics.GenericAPIView
    ):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
class SnippetDetail(
    mixins.RetrieveModelMixin, 
    mixins.UpdateModelMixin, 
    mixins.DestroyModelMixin, 
    generics.GenericAPIView
    ):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
"""


# Best way, generic class-based views:
from django.contrib.auth.models import User
from .models import Snippet
from .serializers import SnippetSerializer, UserSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework import generics
from rest_framework import permissions


class SnippetList(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer