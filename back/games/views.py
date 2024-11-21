from django.shortcuts import get_object_or_404
from django.conf import settings

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import GameQuestion
from movies.models import Genre
from .serializers import GameQuestionSerializer

# Permission Decorators
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

# game
import random

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