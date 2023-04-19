import random

from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from block0.models import Post
from .serializers import PostModelSerializer


# Create your views here.
@api_view(['GET'])
def date_time_test_api(request):
    string = request.GET.get('string') or ''
    if string:
        result = {}
        for i in string:
            try:
                result[i] = int(result.get(i)) + 1
            except TypeError as e:
                result[i] = 1
        return Response(result, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'no string given'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def random_post(request):
    count = request.GET.get('count') or ''
    if count:
        if int(count) <= 0:
            return Response({'error': 'count must be > 0'}, status=status.HTTP_400_BAD_REQUEST)
        all_posts = list(Post.objects.all())
        list_of_posts = random.sample(all_posts, k=(int(count) if int(count) <= len(all_posts) else len(all_posts)))
        serialized = PostModelSerializer(list_of_posts, many=True)
    else:
        post_ = random.choice(Post.objects.all())
        serialized = PostModelSerializer(post_)
    return Response(serialized.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def post(request):
    if request.GET.get('id'):
        if request.GET.get('title'):
            return Response({'error': 'args must be either id or title'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            post_ = Post.objects.filter(pk=int(request.GET.get('id')))
        except Post.DoesNotExist:
            return Response({'error': 'does not exist'}, status=status.HTTP_404_NOT_FOUND)
    elif request.GET.get('title'):
        try:
            post_ = Post.objects.filter(title__contains=request.GET.get('title'))
        except Post.DoesNotExist:
            return Response({'error': 'does not exist'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'error': 'args must be either id or title'}, status=status.HTTP_400_BAD_REQUEST)
    serialized = PostModelSerializer(post_, many=True)
    return Response(serialized.data, status=status.HTTP_200_OK)
