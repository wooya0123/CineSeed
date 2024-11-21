from django.urls import path
from . import views

urlpatterns = [
    path('movies/', views.movie_list),
    path('movies/<int:movie_id>/', views.movies_detail),
    path('movies/<int:movie_id>/likes/', views.likes),
]