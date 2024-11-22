from django.urls import path
from . import views

urlpatterns = [
    path('setting/', views.game_setting),  # 게임 요청을 받고, 게임을 만들어서 주는 url
    path('result/', views.game_result),      # 게임 결과 받아서 칭호 저장하는 url -> 이 url에서 영화 고르기 게임도 만들어서 주어야하나
    path('save-data/', views.set_game_movie_data),
    path('save-addtional-data/', views.set_additional_game_movie_data)
]