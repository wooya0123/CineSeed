from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import GameQuestion
from .serializers import GameQuestionSerializer

# Permission Decorators
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

# game
import random

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # 로그인한 사용자만 게임을 플레이할 수 있음
def game_setting(request):
    game_pk = random(1, 7)              # 질문 세트 pk 번호를 random하게 정하기 -> type는 총 6개
    game_questions = get_object_or_404(GameQuestion, pk=game_pk)

    if request.method == 'GET':
        serializer = GameQuestionSerializer(game_questions)
        return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])  # 로그인한 사용자만 게임을 플레이할 수 있음
def game_title(request):
    # STEP 1.user에 title, genre를 설정
    # 받아온 결과 : g1c1aaaaaa - g2c3bbbbb
    game_result = request.data
    genre_code = game_result[1] + game_result[4:7]    # 1aaa - 2bbb 형식으로 parsing
    category_code = game_result[3] + game_result[7:]  # 1aa - 3bb 형식으로 parsing

    # 사용자 답변으로 genre code 찾아주기 -> 아래 함수에서
    # 사용자 답변으로 genre text 찾아주기 -> genre 모델에서
    # 사용자 답변으로 분류(평론가 등) 찾아주기

    # request.user에 title 저장
    # request.user에 genre pk 값 저장

    # STEP 2. 게임 영화 DB 넘겨주기
    pass

def find_genre(genre_code):
    # return 값 : code와 text
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
    pass

def find_category(category_code):
    # return 값 : 칭호(text)
    code_dict = {
        '1aa': '트랜드 리더',
        '1aa': '예술가',
        '1aa': '수집가',
        '1aa': '평론가',

        '2aa': '예술가',
        '2aa': '평론가',
        '2aa': '트랜드 리더',
        '2aa': '수집가',

        '3aa': '트랜드 리더',
        '3aa': '예술가',
        '3aa': '수집가',
        '3aa': '평론가',
    }
    pass
