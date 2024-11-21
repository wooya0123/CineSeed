from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import Movie


# 전체 db 대상
def movie_list(request):
    # 데이터 조회


    # 데이터 전송, db 수정
    pass

# 단일 데이터 대상
def movies_detail(request):
    movie_id = request.GET.get('movie_id')
    movie = Movie.objects.get(id=movie_id)

    # 단일 데이터 조회


    # 단일 데이터 삭제


    #단일 데이터 수정
