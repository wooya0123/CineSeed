from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import Movie
from .serializers import MovieListSerializer, MovieSerializer, MovieCreateSerializer, MovieUpdateSerializer


# 전체 db 대상(permission은 생각해보기)
@api_view(['GET', 'POST'])
def movie_list(request):
    # 데이터 조회
    if request.method == 'GET':
        movies = Movie.objects.all()
        serializer = MovieListSerializer(movies, many=True)
        return Response(serializer.data)

    # 데이터 전송, db 수정
    elif request.method == 'POST':
        serializer = MovieCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 단일 데이터 대상(permission은 생각해보기)
@api_view(['GET', 'DELETE', 'PUT'])
def movies_detail(request, movie_id):
    movie = Movie.objects.get(pk=movie_id)

    # 단일 데이터 조회
    if request.method == 'GET':
        serializer = MovieSerializer(instance=movie)
        return Response(serializer.data)

    # 단일 데이터 삭제
    elif request.method == 'DELETE':
        movie.delete()

    #단일 데이터 수정
    elif request.method == 'PUT':
        serializer = MovieUpdateSerializer(movie, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)