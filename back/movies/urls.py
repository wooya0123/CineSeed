from django.urls import path
from . import views

urlpatterns = [
    path('', views.movie_list),
    path('<int:movie_id>/', views.movie_detail),
    path('<int:movie_id>/like/', views.like),
    path('<int:movie_id>/fund/', views.fund),
    path('<int:movie_id>/application/',views.application)
]