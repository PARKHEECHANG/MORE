from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from .serializers.movie import MovieSerializer
from .serializers.comment import CommentSerializer, CommetListSerializer, CommentCreateSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Movie, Comment


@api_view(['GET'])
# @permission_classes(['IsAuthenticated'])
def movie_detail(request, movie_pk):
    if request.method == 'GET':
        try:
            movie = get_object_or_404(Movie, pk=movie_pk)
        except:
            movie_data = {
                'movie_id':movie_pk
            }
            movieserializer = MovieSerializer(data=movie_data)
            if movieserializer.is_valid(raise_exception=True):
                movieserializer.save()
                movie = get_object_or_404(Movie, pk=movie_pk)
        comment = get_list_or_404(Comment, movie_id_id = movie_pk)
        serializer = CommetListSerializer(comment, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

@api_view(['POST'])
def comment_create(request, movie_pk):
    print(1)
    movie = get_object_or_404(Movie, pk=movie_pk)
    print(2)
    serializer = CommentSerializer(data=request.data)
    print(request.data)
    if serializer.is_valid(raise_exception=True):
        print(5)
        serializer.save(movie=movie, user=request.user)
        print(4)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        print(3)


@api_view(['PUT', 'DELETE'])
# @permission_classes(['IsAuthenticated'])
def comment_detail(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.method == 'PUT':
        # if request.user == comment.user:
            serializer = CommentCreateSerializer(comment, data=request.data)
            print(serializer)
            if serializer.is_valid(raise_exception=True):
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        # else:
        #     data = {
        #         'update':False,
        #         'description': '로그인한 유저가 작성한 글이 아닙니다.'
        #     }    
        #     return Response(data, status=status.HTTP_401_UNAUTHORIZED)
    elif request.method == 'DELETE':
        # if request.user == comment.user:
            comment.delete()
            data = {
                'delete': f'comment {comment_pk} is deleted'
            }
            return Response(data, status=status.HTTP_204_NO_CONTENT)
        # else:
        #     data = {
        #         'delete':False,
        #         'description': '로그인한 유저가 작성한 글이 아닙니다.'
        #     }    
        #     return Response(data, status=status.HTTP_401_UNAUTHORIZED)