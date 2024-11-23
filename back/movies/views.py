from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import Movie
from accounts.models import FundMovie
from .serializers import MovieListSerializer, MovieSerializer, MovieCreateSerializer, MovieUpdateSerializer, MovieRecommendationSerializer

from django.db.models import Count

# Permission Decorators
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

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
        # 로그인하지 않은 유저는 수정 불가
        if not request.user.is_authenticated:
            return Response({'message': '로그인하지 않은 사용자입니다'}, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = MovieCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 단일 데이터 대상(permission은 생각해보기)
@api_view(['GET', 'DELETE', 'PUT'])
def movie_detail(request, movie_id):
    movie = Movie.objects.get(id=movie_id)

    # 단일 데이터 조회
    if request.method == 'GET':
        serializer = MovieSerializer(instance=movie)
        return Response(serializer.data)

    # 단일 데이터 삭제
    elif request.method == 'DELETE':
        if not request.user.is_authenticated:
            return Response({'message': '로그인하지 않은 사용자입니다'}, status=status.HTTP_401_UNAUTHORIZED)
        
        movie.delete()

    #단일 데이터 수정
    elif request.method == 'PUT':
        if not request.user.is_authenticated:
            return Response({'message': '로그인하지 않은 사용자입니다'}, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = MovieUpdateSerializer(movie, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# 좋아요 기능
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    user = request.user

    # 펀딩글의 작성자가 아닐 때
    if movie.user != request.user.like_movies:
        # 해당 영화가 유저의 좋아요한 영화에 포함되어 있다면
        if movie in request.user.like_movies.all():
            movie.like_users.remove(user)
            message = '좋아요 취소'
            is_liked = False
        else:
            movie.like_users.add(user)
            message = '좋아요 추가'
            is_liked = True
        
        result = {
            'message': message,
            'is_liked': is_liked
        }
        return Response(result)
    return Response({'error': '본인이 작성한 글에는 좋아요를 할 수 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)


# 펀딩 기능
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def fund(request, movie_id):
    user = request.user
    movie = Movie.objects.get(id=movie_id)
    funding = int(request.data.get('cash'))

    # 유저의 cash가 펀딩할 금액 이상일 때 해당 금액 만큼 cash 감소
    if user.cash >= funding:
        user.cash -= funding
        user.save()
        
        # 펀딩 금액만큼 영화 후원 총액 증가
        fund_movie = FundMovie.objects.get_or_create(user=user, movie=movie, defaults={'amount': 0})
        fund_movie = fund_movie[0]
        fund_movie.amount += funding
        fund_movie.save()
        
        return Response({'유저 잔액': user.cash, '유저가 영화에 펀딩한 총액': fund_movie.amount})
    else:
        return Response({'잔액이 부족합니다.'}, status=status.HTTP_400_BAD_REQUEST)
        

# 스탭으로 지원하기 기능
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def application(request, movie_id):
    user = request.user
    movie = Movie.objects.get(id=movie_id)

    # 감독이 아니면, 테이블에 데이터 저장, 지원하면 취소는 불가
    if user.role == 'ST':
        if user in movie.apply_users.all():
            is_applied = True
            pass
        else:
            movie.apply_users.add(user)
            is_applied = True

        result = {
            'message': '지원 완료',
            'is_applied': is_applied
        }
        return Response(result)
    else:
        result = {
            'message': '권한이 없습니다'
        }
        return Response(result)

@api_view(['GET'])
def popular_recommandation(request):
    # 좋아요 순 펀딩 추천
    popular_movies = (
        Movie.objects.annotate(like_count=Count('like_users'))  # 좋아요 개수를 계산 -> 필드 추가
        .order_by('-like_count', '-start_date')[:9]            # 좋아요가 많고, 최신순으로 정렬
    )
    if not popular_movies.exists():
        return Response({"message": "추천할 영화가 없습니다."}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = MovieRecommendationSerializer(popular_movies, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def personalized_recommandation(request):
    # 회원 취향 맞춤 펀딩 추천
    user_preferred_genre = request.user.genre # 사용자의 선호 장르
    print('유저 정보', request.user)
    user_preferred_movies = (
        Movie.objects.filter(genre=user_preferred_genre)    # 사용자가 선호하는 장르 필터
    )

    serializer = MovieRecommendationSerializer(user_preferred_movies, many=True)
    return Response(serializer.data)
