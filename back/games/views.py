from django.shortcuts import get_object_or_404
from django.conf import settings

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import GameQuestion, GameMovie
from movies.models import Genre, Movie
from .serializers import GameQuestionSerializer

# Permission Decorators
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

# game
import random
import requests

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # 로그인한 사용자만 게임을 플레이할 수 있음
def game_setting(request):
    game_pk = random.randint(1, 7)              # 질문 세트 pk 번호를 random하게 정하기 -> type는 총 6개
    game_questions = get_object_or_404(GameQuestion, pk=game_pk)

    if request.method == 'GET':
        serializer = GameQuestionSerializer(game_questions)
        return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])  # 로그인한 사용자만 게임을 플레이할 수 있음
def game_title(request):
    # STEP 1.user에 title, genre를 설정
    # 받아온 결과 : g1c1aaaaa - g2c3bbbbb
    game_result = request.data.get('result')

    genre_code = game_result[1] + game_result[4:7]    # 1aaa - 2bbb 형식으로 parsing
    category_code = game_result[3] + game_result[7:]  # 1aa - 3bb 형식으로 parsing

    # 사용자 답변으로 genre_code 찾아주기 -> 아래 함수에서
    # 1aaa -> A로 바꿔주기
    genre_code = find_genre(genre_code)

    # user_genre에 Genre 객체 저장
    user_genre = Genre.objects.get(code=genre_code)

    # genre_code로 genre_name 찾아주기 -> genre 모델에서
    # A로 '낭만적인' 찾아오기
    genre_name = user_genre.name
    # 사용자 답변으로 분류(평론가 등) 찾아주기
    # 1aa로 '트랜드 리더' 찾아오기
    category_name = find_category(category_code)

    # request.user에 title 저장 
    title = genre_name + ' ' + category_name
    request.user.title = title
    # request.user에 genre 객체 값 저장
    request.user.genre = user_genre
    request.user.save()

    # STEP 2. 게임 영화 DB 넘겨주기

def find_genre(genre_code):
    # return 값 : code
    code_dict = {
        '1aaa': 'A',
        '1aab': 'C',
        '1aba': 'D',
        '1abb': 'B',
        '1baa': 'E',
        '1bab': 'G',
        '1bba': 'H',
        '1bbb': 'F',
        
        '2aaa': 'E',
        '2aab': 'H',
        '2aba': 'B',
        '2abb': 'F',
        '2baa': 'A',
        '2bab': 'C',
        '2bba': 'G',
        '2bbb': 'D',
    }

    return code_dict.get(genre_code)

def find_category(category_code):
    # return 값 : 칭호(name)
    code_dict = {
        '1aa': '트랜드 리더',
        '1ab': '예술가',
        '1ba': '수집가',
        '1bb': '평론가',

        '2aa': '예술가',
        '2ab': '평론가',
        '2ba': '트랜드 리더',
        '2bb': '수집가',

        '3aa': '트랜드 리더',
        '3ab': '예술가',
        '3ba': '수집가',
        '3bb': '평론가',
    }

    return code_dict.get(category_code)

@api_view(['POST'])
def set_game_movie_data(request):
    # TMDB의 genre_id와 우리 장르 분류 관계를 저장한 dict 만들기
    convert_genre = {
        '28' : 'H', # 액션 H
        '12' : 'H', # 모험 H
        '16' : 'G', # 애니메이션 G
        '35' : 'E', # 코미디 E
        '80' : 'H', # 범죄 H
        '99' : 'C', # 다큐멘터리 C
        '18' : 'D', # 드라마 D
        '10751' : 'E', # 가족 E
        '14' : 'G', # 판타지 G
        '36' : 'C', # 역사 C
        '27' : 'F', # 공포 F
        '10402' : 'B', # 음악 B
        '9648' : 'F', # 미스터리 F
        '10749' : 'A', # 로맨스 A
        '878' : 'G', # SF G
        '10770' : 'D', # TV 영화 D
        '53' : 'F', # 스릴러 F
        '10752' : 'H', # 전쟁 H
        '37' : 'H', # 서부 H
    }
    # 영화 이미지 url 앞에 부분
    base_url = "https://image.tmdb.org/t/p/original"
    
    # api에 요청해서 정보 가져오기
    api_key = settings.API_KEY
    url = 'https://api.themoviedb.org/3/movie/top_rated'
    headers = {
        'Authorization': f'Bearer {api_key}'
    }
    params = {
        "api_key": api_key,
        "language": 'ko-KR',
        "region": 'KR',
        "page": 1,
    }
    response = requests.get(url, headers=headers, params=params).json()

    # response에 들어있는 영화를 순회
    for movie in response.get('results'):
        # GameMovie에 들어갈 정보들을 변수에 저장
        title = movie.get('title')
        poster_path = movie.get('poster_path')
        genre_id = movie.get('genre_ids')[0]

        # genre_id를 '우리가 정의한 장르'와 매칭시키기
        genre_id = convert_genre.get(str(genre_id))


        # DB에 저장
        image_url = f"{base_url}{poster_path}"
        new_movie = GameMovie.objects.create(title=title, image=image_url)
        new_movie.genre = Genre.objects.get(code=genre_id)
        new_movie.save()

    return Response(response)